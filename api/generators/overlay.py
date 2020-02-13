from PIL import Image, ImageSequence

from generators import Generator


class OverlayGenerator(Generator):
    ALLOWED_OVERLAYS = {
        "fire.gif": "burning",
        "fire2.gif": "burning",
        "sparkle.gif": "sparkling",
        "sparkle2.gif": "sparkling",
        "loving.gif": "loving",
    }

    def __init__(self):
        super().__init__('overlay', defaults={
            "overlay": "fire.gif"
        })

    def generate(self, original_name, input_path, output_dir, options):
        options = {**self.defaults, **options}
        overlay_file = options["overlay"]

        if overlay_file not in OverlayGenerator.ALLOWED_OVERLAYS:
            raise ValueError("Unknown overlay " + overlay_file)
        overlay_name = OverlayGenerator.ALLOWED_OVERLAYS[overlay_file]

        overlay = Image.open(f"resources/{overlay_file}")
        emoji = self.load_image(input_path)
        emoji = emoji[0]
        emoji_name = Generator.get_emoji_name_from_file(original_name)

        frames = []
        emoji_w, emoji_h = emoji.size
        palette = None
        for i, overlay_frame in enumerate(ImageSequence.Iterator(overlay)):
            canvas = Image.new("RGBA", emoji.size, (255, 255, 255))

            if palette is None:
                palette = overlay_frame.getpalette()
            else:
                overlay_frame.putpalette(palette)

            # overlay_frame.save(f'../output/{overlay_name}.{i:02}.gif', 'GIF')
            # cropped_frame = fire_frame.crop((0, 0, emoji_w, emoji_h))
            overlay_frame.thumbnail(canvas.size)
            overlay_frame = overlay_frame.convert('RGBA')
            canvas.paste(emoji, (0, 0), mask=emoji)

            offset = ((canvas.width - overlay_frame.width) // 2, (canvas.height - overlay_frame.height) // 2)
            if overlay_name == 'burning':
                offset = (0, emoji_h - overlay_frame.height + 5)

            canvas.paste(overlay_frame, offset, mask=overlay_frame)
            frames.append(canvas)

        return self.write_gif(frames, output_dir, emoji_name + ".gif", options), f'{overlay_name}_{original_name}'
