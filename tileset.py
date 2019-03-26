import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf as gdkPixbuf
from gi.repository import GLib as gLib
import array
import cairo
import numpy
from PIL import Image

# Stores all the tiles created. Can be selected and drawn onto canvas to be edited
class Tileset():
  def __init__(self, tile_width, tile_height):
    self.tile_width = tile_width
    self.tile_height = tile_height
    self.tiles = []

  def get_tile_width(self):
    return self.tile_width

  def get_tile_height(self):
    return self.tile_height

  def add(self):
    self.tiles.append(Tile(self.tile_width, self.tile_height))

  def get(self, tile_id):
    return self.tiles[tile_id]

  def remove(self, tile_id):
    del self.tiles[tile_id]

# Single tile. Will be drawn multiple times on canvas
class Tile():
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.img = Image.new('RGB', (width, height), 'black')
    self.img.putalpha(256)
    self.pixels = self.img.load()

  def get_width(self):
    return self.width

  def get_height(self):
    return self.height

  def set_pixel(self, x, y, color):
    self.pixels[x, y] = tuple([x * 255 for x in color])

  def draw(self, ctx, pixel_size, tile_pos):
    tile_x, tile_y = tile_pos
    tmp_img = self.img.resize((self.width * pixel_size, self.height * pixel_size), resample=Image.BOX)
    arr = numpy.array(tmp_img)
    height, width, channels = arr.shape
    surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, width, height)
    # ctx.scale(pixel_size, pixel_size)
    ctx.set_source_surface(surface, tile_x * self.width * pixel_size, tile_y * self.height * pixel_size)
    ctx.rectangle(tile_x * self.width * pixel_size,
        tile_y * self.height * pixel_size,
        self.width * pixel_size,
        self.height * pixel_size)
    ctx.fill()

def create():
  return Tileset(16, 16)
