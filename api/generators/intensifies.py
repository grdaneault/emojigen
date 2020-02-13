import math
import random

from PIL import Image

from generators.generator import Generator


class IntensifiesGenerator(Generator):

    def __init__(self):
        super().__init__('intensifies', defaults={
            "intensity": 7
        })

    def generate(self, original_name, input_path, output_dir, options):
        options = {**self.defaults, **options}
        intensity = int(options['intensity'])

        emoji_name = Generator.get_emoji_name_from_file(original_name)
        source = self.load_image(input_path)

        if len(source) < 6:
            source *= math.ceil(6 / len(source))

        frames = []
        for frame in source:
            frame = frame.copy()
            canvas = Image.new("RGBA", frame.size, color=(255, 255, 255, 255))
            canvas.paste(frame,
                         (random.randrange(-intensity, intensity), random.randrange(-intensity // 4, intensity // 4)),
                         mask=frame)
            frames.append(canvas)

        return self.write_gif(frames, output_dir, emoji_name + ".gif", options), f'{original_name}_intensifies'
