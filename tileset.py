import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf as gdkPixbuf
from gi.repository import GLib as gLib
import array
import cairo
from PIL import Image
import image_button

# Stores all the tiles created. Can be selected and drawn onto canvas to be edited
class Tileset():
  def __init__(self, tile_width, tile_height):
    self.tile_width = tile_width
    self.tile_height = tile_height
    self.tiles = [] # array of Tile objects
    self.selected_tile_id = -1 # index of tile selected in gui
    self.box = gtk.Box(orientation=gtk.Orientation.VERTICAL) # main container for everything
    self.buttons_box = gtk.Box(orientation=gtk.Orientation.HORIZONTAL) # container for add / delete buttons

    self.new_button = image_button.Button("assets/pencil.png")
    self.buttons_box.pack_start(self.new_button.widget(), False, False, 0)
    self.new_button.widget().connect("clicked", self.add)

    self.delete_button = image_button.Button("assets/eraser.png")
    self.buttons_box.pack_start(self.delete_button.widget(), False, False, 0)
    self.delete_button.widget().connect("clicked", self.remove_selected)

    self.da = gtk.DrawingArea() # will draw tiles in here
    self.da.connect("draw", self.draw)
    self.da.set_vexpand(True)
    self.da.set_hexpand(True)
    self.event_box = gtk.EventBox()
    self.event_box.connect("button-press-event", self.click)
    self.event_box.add_events(gdk.EventMask.BUTTON_PRESS_MASK)
    self.event_box.add(self.da)

    self.box.pack_start(self.buttons_box, False, False, 0)
    self.box.pack_start(self.event_box, True, True, 0)
    self.box.show()

    self.pixel_size = 4 # this should be the width of the tileset / tiles_per_row / tile_width
    self.tiles_per_row = 2 # this should be defined based on how big we want the tiles to be

    self.add(None)

  def widget(self):
    return self.box

  def update(self):
    self.da.queue_draw()

  def load_tileset(self, width, height, tileset):
    self.tile_width = width
    self.tile_height = height
    self.tiles = []
    for image in tileset:
      self.add(None)
      tile = self.tiles[len(self.tiles) - 1]
      tile.load_image(image)

  def get_tile_width(self):
    return self.tile_width

  def get_tile_height(self):
    return self.tile_height

  def add(self, event):
    self.tiles.append(Tile(self.tile_width, self.tile_height, len(self.tiles)))
    self.da.queue_draw()

  def get(self, tile_id):
    return self.tiles[tile_id]

  def remove_selected(self, event):
    if self.selected_tile_id == -1:
      return
    tile = self.tiles[self.selected_tile_id]
    tile.destroy()
    del self.tiles[self.selected_tile_id]
    if self.selected_tile_id >= len(self.tiles):
      self.selected_tile_id = -1
    self.da.queue_draw()

  def click(self, widget, event):
    tile_x = int(event.x / self.tile_width / self.pixel_size)
    tile_y = int(event.y / self.tile_height / self.pixel_size)
    index = tile_y * self.tiles_per_row + tile_x
    if index >= len(self.tiles):
      index = -1
    self.selected_tile_id = index
    self.da.queue_draw()

  def draw(self, widget, ctx):
    i = 0
    for tile in self.tiles:
      tile.draw(ctx, self.pixel_size, (i % self.tiles_per_row * 9 / 8, int(i / self.tiles_per_row) * 9 / 8))
      i += 1
    if self.selected_tile_id >= 0:
      x = self.selected_tile_id % self.tiles_per_row * self.tile_width * self.pixel_size
      y = int(self.selected_tile_id / self.tiles_per_row) * self.tile_height * self.pixel_size
      ctx.set_source_rgb(1, 1, 1)
      ctx.rectangle(x * 9 / 8, y * 9 / 8, self.tile_width * self.pixel_size, self.tile_height * self.pixel_size)
      ctx.stroke()

  def get_selected_tile(self):
    return self.selected_tile_id

  def destroy(self):
    raise "no yeetage"
    for tile in self.tiles:
      tile.destroy()
    self.da.destroy()

# Single tile. Will be drawn multiple times on canvas
class Tile():
  def __init__(self, width, height, index):
    self.width = width
    self.height = height
    self.img = Image.new('RGB', (width, height), 'black')
    self.img.putalpha(256)
    self.pixels = self.img.load()
    self.button = gtk.ToggleButton(relief=gtk.ReliefStyle.NORMAL)
    self.button.set_size_request(32, 32 * 1.35)
    self.button.index = index
    self.button_drawing_area = gtk.DrawingArea()
    self.button_drawing_area.connect("draw", self.draw_button)
    self.button_drawing_area.show()
    self.button.add(self.button_drawing_area)
    self.button.show()
    self.update_pattern()

  def update_button(self):
    self.button_drawing_area.queue_draw()

  def destroy(self):
    self.button.destroy()
    self.button_drawing_area.destroy()

  def draw_button(self, widget, ctx):
    mat = cairo.Matrix() # to get rid of the translation on the pattern when drawing on the canvas
    self.pattern.set_matrix(mat)
    ctx.scale(widget.get_allocated_width() / self.img.width,
        widget.get_allocated_height() / self.img.height)
    ctx.set_source(self.pattern)
    ctx.paint()

  def widget(self):
    return self.button

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
    mat.scale(1 / pixel_size, 1 / pixel_size)
    self.pattern.set_matrix(mat)
    ctx.set_source(self.pattern)
    ctx.rectangle(tile_x * self.width * pixel_size,
            tile_y * self.height * pixel_size,
            self.width * pixel_size,
            self.height * pixel_size)
    ctx.fill()

  def __repr__(self):
    return "Tile <index=" + str(self.button.index) + ">"

def create(width, height):
  return Tileset(width, height)
