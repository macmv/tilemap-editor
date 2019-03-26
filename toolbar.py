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

  def get_tileset(self):
    return self.tileset

  def click(self, widget):
    pass

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    self.tools[self.current_tool].draw(ctx, cursor_x, cursor_y, size)

  def widget(self):
    return gtk.Button(label="Click Here")

def create(tileset, tool_settings):
  return Toolbar(tileset, tool_settings)

class Tool():
  def __init__(self):
    pass

  def use(self, canvas, pixel_x, pixel_y):
    pass

  def draw(self, ctx, cursor_x, cursor_y, size):
    pass

class Brush(Tool):
  def __init__(self):
    self.radius = 1
    self.color = (1, 0, 0, 1) # rgba

  def use(self, canvas, pixel_x, pixel_y):
    tile_pos = canvas.get_tileset().pixel_to_tile((pixel_x, pixel_y))
    tile = canvas.get_tile(tile_pos)

  def draw(self, ctx, cursor_x, cursor_y, size):
    ctx.set_source_rgba(1, 0, 0, 1)
    ctx.rectangle(cursor_x, cursor_y, size, size)
    ctx.fill()
