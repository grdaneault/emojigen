import os
from PIL import Image
import random


def intensifies(emoji_file, amount):
    last = os.path.basename(emoji_file)
    emoji_name, ext = os.path.splitext(last)

    source = Image.open(emoji_file)
    frames = []
    for color_hex in range(6):
        frame = source.copy()
        canvas = Image.new("RGBA", frame.size, color=(255, 255, 255, 255))
        canvas.paste(frame, (random.randrange(-amount, amount), random.randrange(-amount // 4, amount // 4)), mask=frame)
        frames.append(canvas)

    args = {
        "save_all": True,
        "append_images": frames[1:],
        "duration": 30,
        "loop": 0,
        "disposal": 2
    }

    frames[0].save(f'../output/{emoji_name}_intensifies.{amount}.gif', **args)

    with open("../output/intensifies_log.html", "a") as log:
        log.write(f'<img src="{emoji_name}_intensifies.{amount}.gif" /> {amount}<br />')


try:
    os.remove("../output/intensifies_log.html")
except:
    pass

for emoji in ['merged', 'bolt']:
    for amount in range(3, 15, 2):
        intensifies(f"/home/greg/dev/emoji/custom_emoji/img/{emoji}.png", amount)
