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
    self.tiles = [] # array of Tile objects
    self.selected_tile_id = 0 # index if tile selected in gui
    self.grid = gtk.Grid() # for GUI
    self.grid_width = 2 # button accros on the grid

  def widget(self):
    return self.grid

  def draw_tiles(self):
    for tile in self.tiles:
      tile.update_button()

  def load_tileset(self, width, height, tileset):
    self.tile_width = width
    self.tile_height = height
    self.tiles = []
    for button in self.grid.get_children():
      self.grid.remove(button)
    index = 0
    for tile_img in tileset:
      self.add()
      tile = self.tiles[len(self.tiles) - 1]
      tile.load_image(tile_img)

  def get_tile_width(self):
    return self.tile_width

  def get_tile_height(self):
    return self.tile_height

  def add(self):
    self.tiles.append(Tile(self.tile_width, self.tile_height))
    new_tile_id = len(self.tiles) - 1
    self.grid.attach(self.tiles[new_tile_id].widget(),
        new_tile_id % self.grid_width,
        int(new_tile_id / self.grid_width),
        1,
        1)

  def get(self, tile_id):
    return self.tiles[tile_id]

  def remove(self, tile_id):
    del self.tiles[tile_id]

  def get_selected_tile():
    return self.selected_tile_id

# Single tile. Will be drawn multiple times on canvas
class Tile():
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.img = Image.new('RGB', (width, height), 'black')
    self.img.putalpha(256)
    self.pixels = self.img.load()
    self.update_pattern()

  def update_button(self):
    self.button_drawing_area.queue_draw()

  def draw_button(self, widget, ctx):
    mat = cairo.Matrix() # to get rid of the translation on the pattern when drawing on the canvas
    self.pattern.set_matrix(mat)
    ctx.scale(widget.get_allocated_width() / self.img.width,
        widget.get_allocated_height() / self.img.height)
    ctx.set_source(self.pattern)
    ctx.paint()

  def widget(self):
    button = gtk.Button(relief=gtk.ReliefStyle.NORMAL)
    button.set_size_request(32, 32 * 1.35)
    self.button_drawing_area = gtk.DrawingArea()
    self.button_drawing_area.connect("draw", self.draw_button)
    self.button_drawing_area.show()
    button.add(self.button_drawing_area)
    button.show()
    return button

  def load_image(self, img):
    if img.width != self.width or img.height != self.height:
      raise "WTF NOT GOOD IMG"
    self.img = img
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

  def get_pixel(self, x, y):
    r, g, b, a = self.pixels[x, y]
    return gdk.Color(r * 256, g * 256, b * 256)

  def set_pixel(self, x, y, color):
    self.pixels[x, y] = (int(color.red / 256), int(color.green / 256), int(color.blue / 256))
    self.update_pattern()

  def draw(self, ctx, pixel_size, tile_pos):
    tile_x, tile_y = tile_pos
    mat = cairo.Matrix() # apparently this needs to be negative ¯\_(ツ)_/¯
    mat.translate(-tile_x * self.width, -tile_y * self.height)
    self.pattern.set_matrix(mat)
    ctx.set_source(self.pattern)
    ctx.rectangle(tile_x * self.width, tile_y * self.height, self.width, self.height)
    ctx.fill()

def create(width, height):
  return Tileset(width, height)
