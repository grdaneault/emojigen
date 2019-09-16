import os
import uuid

import redis
from flask import Flask, request, jsonify, send_file, abort, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config import WindowsConfig
from generators import PartyGenerator, IntensifiesGenerator, Generator, OverlayGenerator
from model import Metadata, MetadataService

KNOWN_GENERATORS = {gen.name: gen for gen in [PartyGenerator(), IntensifiesGenerator(), OverlayGenerator()]}

app = Flask(__name__)
app.config.from_object(WindowsConfig())
CORS(app)

redis_client = redis.from_url(app.config['REDIS_HOST'])
metadata = MetadataService(redis_client)


@app.route("/api/v1/emoji/<emoji_id>", methods=["GET"])
def get_emoji(emoji_id):
    md = metadata.load(id=emoji_id)
    if not md:
        return abort(404)
    return jsonify(md.to_json(include_path=False))


@app.route("/api/v1/emoji/<emoji_id>/original", methods=["GET"])
def get_emoji_image(emoji_id):
    md = metadata.load(id=emoji_id)
    if not md:
        return abort(404)
    if 'download' in request.args:
        _, extension = os.path.splitext(md.path_on_disk)
        return send_file(md.path_on_disk, as_attachment=True, attachment_filename=md.name + extension)
    else:
        return send_file(md.path_on_disk)


@app.route("/api/v1/emoji/<parent_emoji_id>/<type>/<emoji_id>", methods=["GET"])
def get_generated_emoji_image(emoji_id, type, parent_emoji_id):
    md = metadata.load(id=emoji_id, type=type, parent=parent_emoji_id)
    if not md:
        return abort(404)
    if 'download' in request.args:
        return send_file(md.path_on_disk, as_attachment=True, attachment_filename=md.name + '.gif')
    else:
        return send_file(md.path_on_disk)


@app.route("/api/v1/emoji", methods=["POST"])
def upload_emoji():
    if 'emoji' not in request.files:
        return jsonify({"error": "no file uploaded"})

    file = request.files['emoji']
    original_name = file.filename
    token = uuid.uuid4()
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(token))
    os.mkdir(upload_dir)
    file_path = os.path.join(upload_dir, secure_filename(file.filename))
    file.save(file_path)

    emoji_name = Generator.get_emoji_name_from_file(file.filename)

    md = Metadata(
        id=str(token),
        original_name=original_name,
        name=emoji_name,
        path_on_disk=file_path,
        url=url_for('get_emoji_image', emoji_id=str(token)))
    metadata.save(md)

    return jsonify(md.to_json(include_path=False))


@app.route(f"/api/v1/emoji/<emoji_id>/<generator_name>", methods=['POST'])
def generate(emoji_id, generator_name):
    if generator_name not in KNOWN_GENERATORS:
        abort(404)
    generator = KNOWN_GENERATORS[generator_name]
    md = metadata.load(emoji_id)
    if not md:
        return abort(404)

    output, name = generator.generate(
        md.name,
        md.path_on_disk,
        output_dir=app.config['GENERATED_FOLDER'],
        options=request.json or {})

    token = uuid.uuid4()

    generated = Metadata(id=str(token),
                         original_name=md.original_name,
                         name=name,
                         path_on_disk=output,
                         type=generator_name,
                         parent=emoji_id,
                         url=url_for('get_generated_emoji_image',
                                     emoji_id=str(token),
                                     type=generator_name,
                                     parent_emoji_id=emoji_id))
    metadata.save(generated)

    return jsonify(generated.to_json(include_path=True))


if __name__ == '__main__':
    app.run()
