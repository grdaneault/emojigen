import os
import tempfile

from PIL import Image


class Generator(object):
    def __init__(self, name, defaults):
        self.defaults = {
            "frame_duration": 50
        }
        self.defaults.update(defaults)
        self.name = name

    def generate(self, original_name, input_path, output_dir, options):
        pass

    def name(self):
        return self.name

    @staticmethod
    def load_image(input_path):
        frames = []
        img = Image.open(input_path)

        frame_index = 0
        prev_frame = None
        while True:
            if img.width > 128 or img.height > 128:
                img.thumbnail((128, 128))
            canvas = Image.new("RGB", (128, 128), (255, 255, 255))
            offset = ((128 - img.width) // 2, (128 - img.height) // 2)
            if prev_frame:
                canvas.paste(prev_frame, offset)
            prev_frame = canvas
            canvas.paste(img, offset)
            frames.append(canvas)

            try:
                frame_index += 1
                img.seek(frame_index)
            except Exception as e:
                break
        return frames

    @staticmethod
    def get_emoji_name_from_file(original_name):
        filename = os.path.basename(original_name)
        emoji_name, ext = os.path.splitext(filename)
        return emoji_name

    def write_gif(self, frames, output_dir, name, options):
        options = {**self.defaults, **options}

        args = {
            "save_all": True,
            "append_images": frames[1:],
            "duration": int(options["frame_duration"]),
            "loop": 0,
            # "disposal": 2
        }

        fp, name = tempfile.mkstemp(suffix=name, dir=output_dir)
        frames[0].save(name, **args)
        return name
