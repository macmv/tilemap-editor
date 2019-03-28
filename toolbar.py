import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class Toolbar():
  def __init__(self, tileset, tool_settings):
    self.tileset = tileset
    self.tool_settings = tool_settings
    self.current_tool = 0
    self.tools = []
    self.tools.append(Brush())

  def use(self, canvas, x, y):
    self.tools[self.current_tool].use(canvas, x, y, self.tool_settings)

  def get_tileset(self):
    return self.tileset

  def click(self, widget):
    pass

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    self.tools[self.current_tool].draw_cursor(ctx, cursor_x, cursor_y, size)

  def widget(self):
    return gtk.Button(label="Click Here")

def create(tileset, tool_settings):
  return Toolbar(tileset, tool_settings)

class Tool():
  def __init__(self):
    pass

  def use(self, canvas, pixel_x, pixel_y, settings):
    pass

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    pass

class Brush(Tool):
  def __init__(self):
    self.radius = 1
    self.color = (1, 0, 0, 1) # rgba

  def use(self, canvas, pixel_x, pixel_y, settings):
    canvas.set_pixel(pixel_x, pixel_y, settings.get_color())

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    ctx.set_source_rgba(1, 0, 0, 1)
    ctx.rectangle(cursor_x, cursor_y, size, size)
    ctx.fill()

class Eraser(Tool):
  def __init__(self):
    self.radius = 1
    self.color = (1, 0, 0, 1) # rgba

  def use(self, canvas, pixel_x, pixel_y, settings):
    canvas.set_pixel(pixel_x, pixel_y, (0, 0, 0, 0))

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    ctx.set_source_rgba(0.9, 0.9, .9, 1)
    ctx.rectangle(cursor_x, cursor_y, size, size)
    ctx.fill()
