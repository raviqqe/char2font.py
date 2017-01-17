#!/usr/bin/env python

import json
import sys

import docopt
import numpy
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


FOREGROUND_COLOR = 255
BACKGROUND_COLOR = 0


def char_to_image(char, font, *, size):
    empty_image = PIL.Image.new("L", size, color=BACKGROUND_COLOR)

    try:
        image = empty_image.copy()
        PIL.ImageDraw.Draw(image).text((0, 0),
                                       char,
                                       font=font,
                                       fill=FOREGROUND_COLOR)
        return numpy.array(image, dtype=numpy.uint8)
    except UnicodeEncodeError:
        print(("Could not render the unicode character \\u{:04X}"
               .format(ord(char))),
              file=sys.stderr)
        return None


def chars_to_images(chars, font):
    size = tuple(map(max, zip(*[font.getsize(char) for char in chars])))
    pairs = {char: char_to_image(char, font, size=size) for char in chars}
    return {char: image.tolist() for char, image in pairs.items()
            if image is not None and (image != BACKGROUND_COLOR).any()}


def main(args):
    """
    Usage:
      char2font [-s <size>] -f <font_file> <document_file>
      char2font (-h | --help)

    Outputs a map of character to font image in JSON format.

    Options:
      -f --font-file <font_file>    Specify a TTF font file.
      -s --size <size>              Specify font size. [default: 16]
      -h --help                     Show help.
    """

    with open(args['<document_file>']) as phile:
        print(json.dumps(
            chars_to_images(
                {char for char in phile.read()},
                PIL.ImageFont.truetype(args['--font-file'],
                                       size=int(args['--size']))),
            ensure_ascii=False))


if __name__ == '__main__':
    main(docopt.docopt(main.__doc__))
