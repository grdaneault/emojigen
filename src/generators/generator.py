import os
import tempfile


class Generator(object):
    def __init__(self, name):
        self.output_defaults = {
            "duration": 50
        }
        self.name = name

    def generate(self, original_name, file_path, options):
        pass

    def name(self):
        return self.name

    @staticmethod
    def get_emoji_name_from_file(original_name):
        filename = os.path.basename(original_name)
        emoji_name, ext = os.path.splitext(filename)
        return emoji_name

    def write_gif(self, frames, name, options):
        options = {**self.output_defaults, **options}

        args = {
            "save_all": True,
            "append_images": frames[1:],
            "duration": int(options["duration"]),
            "loop": 0,
            "disposal": 2
        }

        fp, name = tempfile.mkstemp(suffix=name, dir='/tmp/generated')
        frames[0].save(name, **args)
        return name
