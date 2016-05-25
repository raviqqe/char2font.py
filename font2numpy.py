#!/usr/bin/env python

import sys
import docopt
import numpy
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont



# constants

foreground_color = 255
background_color = 0
representative_char = 'A'



# functions

def draw_char(orig_image, char, font):
  image = orig_image.copy()

  try:
    PIL.ImageDraw.Draw(image).text(
        (0, 0),
        char,
        font=font,
        fill=foreground_color)
  except UnicodeEncodeError as exception:
    print("Could not render the unicode character \\u{:04X}".format(ord(char)),
          file=sys.stderr)
    return orig_image

  return image


def new_image(size):
  return PIL.Image.new("L", size, color=background_color)


def load_font(filename, ttf_size=16):
  if filename.endswith(".pil"):
    return PIL.ImageFont.load(filename)
  elif filename.endswith(".ttf"):
    return PIL.ImageFont.truetype(filename, size=ttf_size)

  raise ValueError("Invalid file extention of a font file, {}"
                   .format(filename))


def image_to_array(image):
  return numpy.array(image, dtype=numpy.uint8)


def char_to_font(char, font_filename, ttf_size=None):
  font = load_font(font_filename, ttf_size=ttf_size)
  return image_to_array(draw_char(
      new_image(font.getsize(representative_char)),
      char,
      font))


def char_array_to_font_array(char_array, font_filename, ttf_size=None):
  assert char_array.ndim == 1
  return numpy.array([
      char_to_font(chr(code_point), font_filename, ttf_size=ttf_size)
      for code_point in char_array])


def load_char_array(filename):
  char_array = numpy.load(filename)
  assert any(char_array.dtype == data_type
             for data_type in {numpy.uint8, numpy.uint16, numpy.uint32})
  return char_array


def save_font_array(font_array, filename):
  assert font_array.dtype == numpy.uint8
  numpy.save(filename, font_array)



# main routine

def main(args):
  """
  Usage:
    font2array [-s <size>] -f <font_file> <character_array_file> <font_array_file>
    font2array (-h | --help)

  <font_file> must be in PIL or TTF format. (e.g. my_font.pil or your_font.ttf)
  You should need pillow module to generate PIL format font files.

  Options:
    -f --font-file        Specify a font file to render letters with.
    -s --ttf-size <size>  Specify TTF font size. [default: 10]
    -h --help             Show help.
  """

  font_array = char_array_to_font_array(
      load_char_array(args["<character_array_file>"]),
      args["<font_file>"],
      ttf_size=int(args["--ttf-size"]))

  save_font_array(font_array, args["<font_array_file>"])


if __name__ == "__main__":
  main(docopt.docopt(main.__doc__))
