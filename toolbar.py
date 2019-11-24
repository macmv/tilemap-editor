import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkPixbuf
from gi.repository import Gdk as gdk
import cairo
import image_button

class Toolbar():
  def __init__(self, window, tileset, tool_settings):
    self.tileset = tileset
    self.tool_settings = tool_settings
    self.prev_tool = 1
    self.current_tool = 1
    self.tools = []
    self.tools.append(ColorPicker(0))
    self.tools.append(Brush(1))
    self.tools.append(Eraser(2))
    self.tools.append(TilePlacer(3))
    self.keys_down = set()
    self.grid = gtk.Grid()
    i = 0
    for tool in self.tools: # for a 2 wide grid
      button = tool.widget()
      button.connect("clicked", self.click)
      self.grid.attach(button, i % 2, i / 2, 1, 1)
      i += 1
    self.tools[self.current_tool].widget().set_active(True)

  def set_tileset(self, tileset):
    self.tileset = tileset

  def key_press(self, widget, event):
    key = chr(gdk.keyval_to_unicode(event.keyval))
    # need to use keyval because control, shift, etc.
    self.keys_down.add(event.keyval)
    if key == 'b':
      self.set_tool(1)
    if key == 'e':
      self.set_tool(2)
    if key == 'v':
      self.set_tool(3)

  def key_release(self, widget, event):
    self.keys_down.remove(event.keyval)

  def use(self, canvas, x, y):
    if 65507 in self.keys_down:
      self.tools[0].use(canvas, x, y, self.tool_settings)
    else:
      self.tools[self.current_tool].use(canvas, x, y, self.tool_settings)

  def get_tileset(self):
    return self.tileset

  def set_tool(self, index):
    print("SETTING TOOL", index)
    # deels with the fact that set_active creates a click event
    if index == self.prev_tool:
      return
    self.prev_tool = self.current_tool
    self.current_tool = index
    i = 0
    for tool in self.tools:
      if i != self.current_tool:
        tool.widget().set_active(False)
      i += 1
    self.tools[self.current_tool].widget().set_active(True)

  def click(self, widget):
    self.set_tool(widget.index)

  def draw_cursor(self, ctx, cursor_x, cursor_y, canvas):
    if 65507 in self.keys_down:
      self.tools[0].draw_cursor(ctx, cursor_x, cursor_y, self.tool_settings.get_size(), canvas)
    else:
      self.tools[self.current_tool].draw_cursor(ctx, cursor_x, cursor_y, self.tool_settings.get_size(), canvas)

  def widget(self):
    return self.grid

def create(window, tileset, tool_settings):
  return Toolbar(window, tileset, tool_settings)

class Tool():
  def __init__(self, index):
    self.button = image_button.ToggleButton(self.button_path)
    self.button.widget().index = index

  def use(self, canvas, pixel_x, pixel_y, settings):
    pass

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    pass

  def widget(self):
    return self.button.widget()

  def draw_button(self, widget, ctx):
    self.button.draw_button(widget, ctx)

class Brush(Tool):
  def __init__(self, index):
    self.index = index
    self.button_path = "./assets/pencil.png"
    Tool.__init__(self, index)

  def use(self, canvas, pixel_x, pixel_y, settings):
    for x in range(int(pixel_x - settings.get_size() / 2 + 0.5), int(pixel_x + settings.get_size() / 2 + 0.5)):
      for y in range(int(pixel_y - settings.get_size() / 2 + 0.5), int(pixel_y + settings.get_size() / 2 + 0.5)):
        canvas.set_pixel(x, y, settings.get_color())

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    ctx.set_source_rgba(0.4, 0.8, 0.4, 1)
    ctx.rectangle(int(cursor_x - size / 2 + 0.5), int(cursor_y - size / 2 + 0.5), size, size)
    ctx.fill()

class ColorPicker(Tool):
  def __init__(self, index):
    self.index = index
    self.button_path = "./assets/eye-dropper.png"
    Tool.__init__(self, index)

  def use(self, canvas, pixel_x, pixel_y, settings):
    settings.set_color(canvas.get_pixel(pixel_x, pixel_y))

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    ctx.set_source_rgba(0.4, 0.4, 1, 1)
    ctx.rectangle(int(cursor_x - size / 2 + 0.5), int(cursor_y - size / 2 + 0.5), size, size)
    ctx.fill()

class Eraser(Tool):
  def __init__(self, index):
    self.index = index
    self.button_path = "./assets/eraser.png"
    self.radius = 1
    Tool.__init__(self, index)

  def use(self, canvas, pixel_x, pixel_y, settings):
    canvas.set_pixel(pixel_x, pixel_y, gdk.Color(0, 0, 0))

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    ctx.set_source_rgba(1, 0.4, 0.4, 1)
    ctx.rectangle(int(cursor_x - size / 2 + 0.5), int(cursor_y - size / 2 + 0.5), size, size)
    ctx.fill()

class TilePlacer(Tool):
  def __init__(self, index):
    self.index = index
    self.button_path = "./assets/pencil.png"
    self.radius = 1
    Tool.__init__(self, index)

  def use(self, canvas, pixel_x, pixel_y, settings):
    selected_index = canvas.get_tileset().get_selected_tile()
    canvas.place_tile(int(pixel_x / canvas.get_tileset().get_tile_width()),
        int(pixel_y / canvas.get_tileset().get_tile_height()),
        selected_index)

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    ctx.set_source_rgba(0.4, 0.4, 1, 1)
    x = int(cursor_x / canvas.get_tileset().get_tile_width())
    y = int(cursor_y / canvas.get_tileset().get_tile_height())
    ctx.rectangle(x * canvas.get_toolbar().get_tileset().tile_width,
        y * canvas.get_toolbar().get_tileset().tile_height,
        canvas.get_toolbar().get_tileset().tile_width,
        canvas.get_toolbar().get_tileset().tile_height)
    ctx.fill()
