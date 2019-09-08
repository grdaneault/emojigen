from PIL import Image, ImageSequence
from alpha_helper import alpha_composite_with_color

def divide_chunks(l, n):

    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def normalize_alpha(image):
    data = image.getdata()
    transparent = [d for d in data if d[3] < 128]
    data = [d if d[3] > 128 else (0, 0, 0, 0) for d in data]
    image.putdata(data)


def overlay_emoji(overlay_name, emoji_name):
    overlay = Image.open(f"../resources/{overlay_name}.gif")
    emoji = Image.open(f"/home/greg/dev/emoji/custom_emoji/img/{emoji_name}.png").convert("RGBA")
    # emoji = Image.open("/home/greg/confer.gif").convert("RGBA")
    emoji.load()
    emoji.save(f'../output/{overlay_name}_{emoji_name}.orig.png', 'png')
    emoji.save(f'../output/{overlay_name}_{emoji_name}.orig.gif', 'gif')

    images = []

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
        canvas.paste(overlay_frame, (0, emoji_h - overlay_frame.height + 5), mask=overlay_frame)
        images.append(canvas)
    args = {
        "save_all": True,
        "append_images": images[1:],
        "duration": 100,
        "loop": 0,
        "disposal": 2
    }

    images[0].save(f'../output/{overlay_name}_{emoji_name}.gif',
                   **args)
    # for i, frame in enumerate(images):
    #     frame.save(f'../output/{overlay_name}_{emoji_name}.{i:02}.gif')
    with open(f'../output/{overlay_name}_{emoji_name}.html', 'w') as report:
        for line in open('../resources/view.html'):
            report.write(line.replace("%overlay%", overlay_name).replace("%emoji%", emoji_name))


for overlay in ['fire']:
    old_list = ['bolt', 'cb-response', 'merged', '00', 'apple', 'ship_it_parrot']
    for emoji in old_list:
        overlay_emoji(overlay, emoji)



