import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GdkPixbuf as gdkPixbuf
from gi.repository import Gdk as gdk
import cairo

class Toolbar():
  def __init__(self, window, tileset, tool_settings):
    self.tileset = tileset
    self.tool_settings = tool_settings
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
    self.tools[self.current_tool].button.set_active(True)

  def set_tileset(self, tileset):
    self.tileset = tileset

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
    self.current_tool = widget.index
    i = 0
    for tool in self.tools:
      if i != self.current_tool:
        tool.button.set_active(False)
      i += 1
    self.tools[self.current_tool].button.set_active(True)

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
    self.button_surface = cairo.ImageSurface.create_from_png(self.button_path)
    self.button_pattern = cairo.SurfacePattern(self.button_surface)
    self.button = gtk.ToggleButton()
    self.button.set_size_request(32, 32 * 1.35)
    self.button.index = self.index
    da = gtk.DrawingArea()
    da.connect("draw", self.draw_button)
    self.button.add(da)

  def use(self, canvas, pixel_x, pixel_y, settings):
    pass

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    pass

  def widget(self):
    return self.button

  def draw_button(self, widget, ctx):
    ctx.scale(widget.get_allocated_width() / self.button_surface.get_width(),
        widget.get_allocated_height() / self.button_surface.get_height())
    ctx.set_source(self.button_pattern)
    ctx.paint()

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
