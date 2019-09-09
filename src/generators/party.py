import math

from PIL import Image, ImageColor

from generators.generator import Generator


class PartyGenerator(Generator):

    def __init__(self):
        super().__init__('party', defaults={
            "target_color": "#000000",
            "colors": ['#D50000', '#FF6D00', '#FFAB00', '#AEEA00', '#64DD17', '#00BFA5', '#0091EA', '#304FFE',
                       '#AA00FF'],
            "tolerance": 300
        })

    @staticmethod
    def distance(c1, c2):
        (r1, g1, b1) = c1[0:3]
        (r2, g2, b2) = c2[0:3]
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    @staticmethod
    def replace_color(image, source, replacement, tolerance):
        def replace(pixel):
            if PartyGenerator.distance(pixel, source) < tolerance:
                return replacement + (pixel[3],)
            else:
                return pixel

        data = image.getdata()
        data = [replace(d) for d in data]
        image.putdata(data)

    def generate(self, original_name, input_path, output_dir, options):
        options = {**self.defaults, **options}

        emoji_name = Generator.get_emoji_name_from_file(original_name)
        source = Image.open(input_path).convert("RGBA")
        target_color = ImageColor.getrgb(options['target_color'])
        frames = []
        for color_hex in options['colors']:
            replacement_color = ImageColor.getrgb(color_hex)
            frame = source.copy()
            PartyGenerator.replace_color(frame, target_color, replacement_color, options['tolerance'])
            canvas = Image.new("RGBA", frame.size, color=(255, 255, 255, 255))
            canvas.paste(frame, (0, 0), mask=frame)
            frames.append(canvas)

        return self.write_gif(frames, output_dir, emoji_name + ".gif", options), f'party_{original_name}'
