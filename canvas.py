import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import cairo

# Stores all the tiles arranged in a grid. Also renders everything
class Canvas():
  def __init__(self, toolbar): # Toolbar instance. Will contain selected tool from left side
    self.toolbar = toolbar
    self.tileset = self.toolbar.get_tileset()
    self.canvas = gtk.DrawingArea()
    self.canvas.set_size_request(1536, 864) # 0.8 * 1080p
    self.canvas.set_hexpand(True)
    self.canvas.set_vexpand(True)
    # self.canvas.set_redraw(True)
    self.canvas.connect("draw", self.draw)
    self.event_box = gtk.EventBox()
    self.event_box.connect("button-press-event", self.click)
    self.event_box.connect("button-release-event", self.release)
    self.event_box.connect("motion-notify-event", self.move)
    self.event_box.connect("scroll-event", self.scroll)
    self.event_box.add_events(
        gdk.EventMask.BUTTON_PRESS_MASK
      | gdk.EventMask.BUTTON_RELEASE_MASK
      | gdk.EventMask.POINTER_MOTION_MASK
      | gdk.EventMask.SCROLL_MASK)
    self.event_box.add(self.canvas)
    self.pixel_x = 0
    self.pixel_y = 0
    self.offset_x = 0
    self.offset_y = 0
    self.cursor_x = 0
    self.cursor_y = 0
    self.pixel_size = 10.0 # each pixel is 10 times as large
    self.button_left_down = False
    self.button_middle_down = False
    self.tilemap = {} # looks like: (x, y) -> tile_id
    self.tilemap[(0, 0)] = 0
    self.tilemap[(1, 0)] = 0
    self.tilemap[(2, 0)] = 0
    self.tilemap[(2, 1)] = 0
    self.tilemap[(3, 0)] = 0
    self.tilemap[(4, 0)] = 0
    self.tileset.add()

  def update(self):
    if self.button_left_down:
      tile_x = int(self.pixel_x / self.tileset.get_tile_width())
      tile_y = int(self.pixel_y / self.tileset.get_tile_height())
      tile_pos = (tile_x, tile_y)
      if tile_pos in self.tilemap:
        tile_id = self.tilemap[tile_pos]
        tile = self.tileset.get(tile_id)
        tile.set_pixel(self.pixel_x % self.tileset.get_tile_width(),
            self.pixel_y % self.tileset.get_tile_height(),
            (1, 0, 0, 1))

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
    # self.tilemap[(1, 0)] = 0
    # self.tilemap[(0, 1)] = 0
    self.update()
    widget.queue_draw()

  def scroll(self, widget, event):
    if event.direction == gdk.ScrollDirection.UP:
      self.pixel_size += self.pixel_size * 0.1
      self.offset_x -= (0.1 * (self.cursor_x - self.offset_x))
      self.offset_y -= (0.1 * (self.cursor_y - self.offset_y))
    else:
      self.pixel_size -= self.pixel_size * 0.1
      self.offset_x += (0.1 * (self.cursor_x - self.offset_x))
      self.offset_y += (0.1 * (self.cursor_y - self.offset_y))
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

  def draw(self, widget, ctx):
    print(self.offset_x)
    ctx.translate(self.offset_x, self.offset_y)
    ctx.scale(self.pixel_size, self.pixel_size)
    ctx.set_antialias(cairo.ANTIALIAS_NONE)
    style = widget.get_style_context()
    width = widget.get_allocated_width()
    height = widget.get_allocated_height()
    gtk.render_background(style, ctx, 0, 0, width, height)

    for tile_pos, tile_id in self.tilemap.items():
      tile = self.tileset.get(tile_id)
      tile.draw(ctx, self.pixel_size, tile_pos)
    self.toolbar.draw_cursor(ctx, self.pixel_x, self.pixel_y, 1)

  def widget(self):
    return self.event_box

  def open(self, filename):
    pass

  def save(self, filename):
    pass

def create(toolbar):
  return Canvas(toolbar)
