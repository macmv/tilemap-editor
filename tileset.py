import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf as gdkPixbuf
from gi.repository import GLib as gLib
import array
import cairo
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
    self.update_pattern()

  def update_pattern(self):
    arr = bytearray(self.img.tobytes('raw', 'BGRa'))
    surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, self.img.width, self.img.height)
    self.pattern = cairo.SurfacePattern(surface)
    self.pattern.set_filter(cairo.FILTER_NEAREST)

  def get_width(self):
    return self.width

  def get_height(self):
    return self.height

  def set_pixel(self, x, y, color):
    self.pixels[x, y] = tuple([x * 255 for x in color])
    self.update_pattern()

  def draw(self, ctx, pixel_size, tile_pos):
    tile_x, tile_y = tile_pos
    ctx.translate(tile_x * self.width,
        tile_y * self.height)
    ctx.set_source(self.pattern)
    ctx.rectangle(0,0,
        self.width,
        self.height)
    ctx.fill()
    ctx.translate(-tile_x * self.width,
        -tile_y * self.height)

def create():
  return Tileset(16, 16)
