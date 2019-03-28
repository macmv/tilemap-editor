import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class Toolbar():
  def __init__(self, window, tileset, tool_settings):
    self.tileset = tileset
    self.tool_settings = tool_settings
    self.current_tool = 1
    self.tools = []
    self.tools.append(ColorPicker())
    self.tools.append(Brush())
    self.tools.append(Eraser())
    self.keys_down = set()

  def key_press(self, widget, event):
    self.keys_down.add(event.keyval)

  def key_release(self, widget, event):
    self.keys_down.remove(event.keyval)

  def use(self, canvas, x, y):
    if 65507 in self.keys_down:
      self.tools[0].use(canvas, x, y, self.tool_settings)
    else:
      self.tools[self.current_tool].use(canvas, x, y, self.tool_settings)

  def get_tileset(self):
    return self.tileset

  def click(self, widget):
    pass

  def draw_cursor(self, ctx, cursor_x, cursor_y):
    if 65507 in self.keys_down:
      self.tools[0].draw_cursor(ctx, cursor_x, cursor_y, self.tool_settings.get_size())
    else:
      self.tools[self.current_tool].draw_cursor(ctx, cursor_x, cursor_y, self.tool_settings.get_size())

  def widget(self):
    return gtk.Button(label="Click Here")

def create(window, tileset, tool_settings):
  return Toolbar(window, tileset, tool_settings)

class Tool():
  def __init__(self):
    pass

  def use(self, canvas, pixel_x, pixel_y, settings):
    pass

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    pass

class Brush(Tool):
  def __init__(self):
    pass

  def use(self, canvas, pixel_x, pixel_y, settings):
    for x in range(int(pixel_x - settings.get_size() / 2 + 0.5), int(pixel_x + settings.get_size() / 2 + 0.5)):
      for y in range(int(pixel_y - settings.get_size() / 2 + 0.5), int(pixel_y + settings.get_size() / 2 + 0.5)):
        canvas.set_pixel(x, y, settings.get_color())

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    ctx.set_source_rgba(0.8, 0.8, 0.8, 1)
    ctx.rectangle(int(cursor_x - size / 2 + 0.5), int(cursor_y - size / 2 + 0.5), size, size)
    ctx.fill()

class ColorPicker(Tool):
  def __init__(self):
    pass

  def use(self, canvas, pixel_x, pixel_y, settings):
    settings.set_color(canvas.get_pixel(pixel_x, pixel_y))

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    ctx.set_source_rgba(0.4, 0.4, 1, 1)
    ctx.rectangle(int(cursor_x - size / 2 + 0.5), int(cursor_y - size / 2 + 0.5), size, size)
    ctx.fill()

class Eraser(Tool):
  def __init__(self):
    self.radius = 1
    self.color = (1, 0, 0, 1) # rgba

  def use(self, canvas, pixel_x, pixel_y, settings):
    canvas.set_pixel(pixel_x, pixel_y, (0, 0, 0, 0))

  def draw_cursor(self, ctx, cursor_x, cursor_y, size):
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.rectangle(cursor_x, cursor_y, size, size)
    ctx.fill()
