import requests
from PIL import Image, ImageFont, ImageDraw
import threading
from io import BytesIO
import os
import sys
from textwrap import wrap
import base64
import math
from typing import List


directory = os.path.dirname(sys.argv[0])
os.chdir(directory)

anime_font = ImageFont.truetype('fonts/Cartwheel.otf', 16)
info_font = ImageFont.truetype('fonts/Orator Std Medium.ttf', 13)


class BotImageElement:
    def __init__(self, title, image_info, image_url, is_hentai=False):
        self.title = title
        self.image_info = image_info
        self.image_url = image_url
        self.is_hentai = is_hentai


def get_list_image(elements: List[BotImageElement], header_text: str):
    images = [None] * len(elements)
    threads = [threading.Thread(target=get_anime_image_item,
                                args=[elements[i], i, images]) for i in
               range(len(elements))]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    per_line = math.ceil(math.sqrt(len(elements)))
    margin_horizontal = 30
    margin_vertical = 20

    max_width = max([image.width for image in images])
    max_height = max([image.height for image in images])

    # Making header
    header_text = '\n'.join(wrap(header_text, 32))
    header_width = (max_width * per_line) + (
            margin_horizontal * (per_line + 1))
    font_size_test = Image.new('RGB', (100, 100), (0, 0, 0))
    font_size = 12 * per_line
    header_font = ImageFont.truetype('fonts/Orator Std Medium.ttf', font_size)
    font_size_test_draw = ImageDraw.Draw(font_size_test)

    tw, th = font_size_test_draw.textsize(header_text, font=header_font)
    header_height = th + 30
    header_back = Image.new('RGB', (header_width, header_height),
                            (230, 230, 230))
    header_draw = ImageDraw.Draw(header_back)
    tW, tH = header_back.size
    header_draw.multiline_text(  # Putting name on center
        ((tW - tw) // 2, (tH - th) // 2),
        header_text, font=header_font, spacing=5, align='center',
        fill=(0, 0, 0))

    # Making background
    back_width = header_width
    back_height = max_height * math.ceil(len(elements) / per_line) + (
            margin_vertical * math.ceil(len(elements) / per_line + 1)) + \
                  header_height

    background = Image.new('RGB', (back_width, back_height), (50, 50, 50))
    background.paste(header_back, (0, 0))
    jump = [margin_horizontal, margin_vertical + header_height]
    i = 1
    for image in images:
        background.paste(image, tuple(jump))
        jump[0] += max_width + margin_horizontal
        if i % per_line == 0:
            jump[0] = margin_horizontal
            jump[1] += max_height + margin_vertical
        i += 1
    buffered = BytesIO()
    background.save(buffered, format='JPEG')
    return base64.b64encode(buffered.getvalue()).decode()


def get_anime_image_item(element: BotImageElement, index: int, images):
    img_url = element.image_url
    img_pad = 1
    img_back_width = 225 + img_pad  # Max width on MAL is 225
    img_back_height = 350 + img_pad  # Max height on MAL is 350

    image = Image.open(BytesIO(requests.get(img_url).content))

    img_back = Image.new('RGB', (img_back_width, img_back_height),
                         (60, 60, 60))

    # Making the title with transparent black background
    title_back = Image.new('RGBA', (img_back.width, img_back.height // 4),
                           (0, 0, 0, 200))
    title_draw = ImageDraw.Draw(title_back)
    title = element.title
    title = '\n'.join(wrap(title, 25))  # Limiting big anime titles
    tw, th = title_draw.textsize(title, font=anime_font)
    tW, tH = title_back.size
    title_draw.multiline_text(  # Putting name on center
        ((tW - tw) // 2, (tH - th) // 2), title, font=anime_font, spacing=1,
        align='center')

    # Making the episode and score with transparent black background
    draw = ImageDraw.Draw(img_back)
    info_text = element.image_info
    info_pad = 15
    iw, ih = draw.textsize(info_text, info_font)
    info_back = Image.new('RGBA', (iw + info_pad, ih + info_pad),
                          (0, 0, 0, 200))
    iW, iH = info_back.size

    info_draw = ImageDraw.Draw(info_back)
    info_draw.multiline_text(  # Putting name on center
        ((iW - iw) // 2, (iH - ih) // 2),
        info_text, font=info_font, spacing=5)

    # Getting the place to put image on background center
    back_center = (
        (img_back.width - image.width) // 2,
        (img_back.height - image.height) // 2)

    # Placing anime title and image
    img_back.paste(image, back_center)
    img_back.paste(title_back, (0, img_back.height - title_back.height),
                   title_back)
    img_back.paste(info_back, (0, 0), info_back)
    images[index] = img_back
