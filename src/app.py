import os

from flask import Flask, request, jsonify, url_for, send_file
from werkzeug.utils import secure_filename, redirect

from generators import PartyGenerator

KNOWN_GENERATORS = [PartyGenerator()]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['GENERATED_FOLDER'] = '/tmp/generated'

for generator in KNOWN_GENERATORS:
    @app.route(f"/generate/{generator.name}", methods=['POST'])
    def generate():
        if 'emoji' not in request.files:
            return jsonify({"error": "no file uploaded"})

        file = request.files['emoji']

        file_name = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)

        output = generator.generate(file_name, file_path, {})
        return send_file(output)

@app.route("/")
def index():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data action=/generate/party>
      <input type=file name=emoji>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run()