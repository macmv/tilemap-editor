import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import cairo
import file_manager

# Stores all the tiles arranged in a grid. Also renders everything
class Canvas():
  def __init__(self, window, toolbar): # Toolbar instance. Will contain selected tool from left side
    self.toolbar = toolbar
    self.tileset = self.toolbar.get_tileset()
    self.pixel_x = 0
    self.pixel_y = 0
    self.offset_x = 0.0
    self.offset_y = 0.0
    self.cursor_x = 0
    self.cursor_y = 0
    self.pixel_size = 10.0 # each pixel is 10 times as large
    self.button_left_down = False
    self.button_middle_down = False
    self.width = 0
    self.height = 0
    self.tilemap = {} # looks like: (x, y) -> tile_id
    self.keys_down = set()
    self.fm = file_manager.FileManager(self)

  def place_tile(self, x, y, id):
    if x < self.width and x >= 0 and y < self.height and y >= 0:
      self.tilemap[(x, y)] = id

  def get_toolbar(self):
    return self.toolbar

  def load_from_file(self, filename):
    tileset, proto = self.fm.open(filename)
    self.tileset.load_tileset(proto.tile_width, proto.tile_height, tileset)
    self.width = proto.width
    self.height = proto.height
    self.tilemap = {}
    for index in proto.tiles:
      self.tilemap[(index % self.width, int(index / self.width))] = proto.tiles[index]

  def save(self, filename):
    self.fm.save(filename)

  def update(self):
    if self.button_left_down:
      self.toolbar.use(self, self.pixel_x, self.pixel_y)

  def draw(self, widget, ctx):
    ctx.translate(self.offset_x, self.offset_y)
    ctx.scale(self.pixel_size, self.pixel_size)
    ctx.set_antialias(cairo.ANTIALIAS_NONE)
    style = widget.get_style_context()
    width = widget.get_allocated_width()
    height = widget.get_allocated_height()
    self.draw_background(widget, ctx)

    for tile_pos, tile_id in self.tilemap.items():
      tile = self.tileset.get(tile_id)
      # already transforming ctx, don't want to transform tile, so use 1 for pixel size
      tile.draw(ctx, 1, tile_pos)
    self.toolbar.draw_cursor(ctx, self.pixel_x, self.pixel_y, self)
    self.tileset.draw_tiles()

  def draw_background(self, widget, ctx):
    ctx.set_source_rgba(1, 1, 1, 1)
    for x in range(self.width * 4):
      for y in range(self.height * 4):
        if (x + y) % 2 == 0:
          ctx.rectangle(x * self.tileset.tile_width / 4,
              y * self.tileset.tile_height / 4,
              self.tileset.tile_width / 4,
              self.tileset.tile_height / 4)
    ctx.fill()
    ctx.set_source_rgba(0.8, 0.8, 0.8, 1)
    for x in range(self.width * 4):
      for y in range(self.height * 4):
        if (x + y) % 2 == 1:
          ctx.rectangle(x * self.tileset.tile_width / 4,
              y * self.tileset.tile_height / 4,
              self.tileset.tile_width / 4,
              self.tileset.tile_height / 4)
    ctx.fill()

  def key_press(self, widget, event):
    self.keys_down.add(event.keyval)
    self.toolbar.key_press(widget, event)
    self.update()
    widget.queue_draw()

  def key_release(self, widget, event):
    self.keys_down.remove(event.keyval)
    self.toolbar.key_release(widget, event)
    self.update()
    widget.queue_draw()

  def get_tileset(self):
    return self.tileset

  def get_pixel(self, pixel_x, pixel_y):
    tile_x = int(pixel_x / self.tileset.get_tile_width())
    tile_y = int(pixel_y / self.tileset.get_tile_height())
    tile_pos = (tile_x, tile_y)
    if tile_pos in self.tilemap:
      tile_id = self.tilemap[tile_pos]
      tile = self.tileset.get(tile_id)
      return tile.get_pixel(pixel_x % self.tileset.get_tile_width(),
          pixel_y % self.tileset.get_tile_height())

  def set_pixel(self, pixel_x, pixel_y, color):
    tile_x = int(pixel_x / self.tileset.get_tile_width())
    tile_y = int(pixel_y / self.tileset.get_tile_height())
    tile_pos = (tile_x, tile_y)
    if tile_pos in self.tilemap:
      tile_id = self.tilemap[tile_pos]
      tile = self.tileset.get(tile_id)
      tile.set_pixel(pixel_x % self.tileset.get_tile_width(),
          pixel_y % self.tileset.get_tile_height(),
          color)

  def release(self, widget, event):
    if event.button == 2:
      self.button_middle_down = False
    if event.button == 1:
      self.button_left_down = False

  def click(self, widget, event):
    if event.button == 2:
      self.button_middle_down = True
    if event.button == 1:
      self.button_left_down = True
    self.update()
    widget.queue_draw()

  def scroll(self, widget, event):
    if 65507 in self.keys_down:
      if event.direction == gdk.ScrollDirection.UP:
        self.toolbar.tool_settings.set_size(self.toolbar.tool_settings.get_size() + 1)
      else:
        self.toolbar.tool_settings.set_size(self.toolbar.tool_settings.get_size() - 1)
    else:
      zoom_amount = 0.1
      if event.direction == gdk.ScrollDirection.UP:
        self.pixel_size += self.pixel_size * zoom_amount
        self.offset_x -= (zoom_amount * (self.cursor_x - self.offset_x))
        self.offset_y -= (zoom_amount * (self.cursor_y - self.offset_y))
      else:
        self.pixel_size -= self.pixel_size * zoom_amount
        self.offset_x += (zoom_amount * (self.cursor_x - self.offset_x))
        self.offset_y += (zoom_amount * (self.cursor_y - self.offset_y))
    self.update()
    widget.queue_draw()

  def move(self, widget, event):
    self.pixel_x = int((event.x - self.offset_x) / self.pixel_size)
    self.pixel_y = int((event.y - self.offset_y) / self.pixel_size)
    if self.button_middle_down:
      self.offset_x -= self.cursor_x - event.x
      self.offset_y -= self.cursor_y - event.y
    self.cursor_x = event.x
    self.cursor_y = event.y
    self.update()
    widget.queue_draw()

def load_from_file(filename, window, toolbar):
  c = Canvas(window, toolbar)
  c.load_from_file(filename)
  return c

def load_from_settings(width, height, window, toolbar):
  c = Canvas(window, toolbar)
  c.width = width
  c.height = height
  return c
