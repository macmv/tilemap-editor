import wx
import cairo
import image_button

class Toolbar():
  def __init__(self, pnl, tileset, tool_settings):
    self.tileset = tileset
    self.tool_settings = tool_settings
    self.prev_tool = 1
    self.current_tool = 1
    self.tools = []
    self.box = wx.Panel(pnl)
    self.tools.append(ColorPicker(0, self))
    self.tools.append(Brush      (1, self))
    self.tools.append(Eraser     (2, self))
    self.tools.append(TilePlacer (3, self))
    sizer = wx.GridBagSizer()
    self.box.SetSizer(sizer)
    i = 0
    for tool in self.tools:
      button = tool.widget()
      sizer.Add(button, pos=(int(i / 2), i % 2), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
      i += 1
    sizer.AddGrowableCol(0)
    sizer.AddGrowableCol(1)
    self.tools[self.current_tool].widget().SetValue(True)

  def set_tileset(self, tileset):
    self.tileset = tileset

  def key_press(self, event):
    key = chr(event.GetUnicodeKey())
    # need to use keyval because control, shift, etc.
    if key == 'B':
      self.set_tool(1)
    if key == 'E':
      self.set_tool(2)
    if key == 'V':
      self.set_tool(3)
    if key == 'N':
      self.tileset.add(None)
    if ord(key) >= 48 and ord(key) <= 58: # if you pressed any number
      # 48 is key 0, 49 is key 1
      # key 0 -> tile 10
      index = ord(key) - 49
      if index == -1:
        index = 9
      self.tileset.select(index) # set the selected tile to that number
      self.set_tool(3)

  def use(self, canvas, x, y):
    if wx.GetKeyState(wx.WXK_CONTROL):
      self.tools[0].use(canvas, x, y, self.tool_settings)
    else:
      self.tools[self.current_tool].use(canvas, x, y, self.tool_settings)

  def get_tileset(self):
    return self.tileset

  def set_tool(self, index):
    self.prev_tool = self.current_tool
    self.current_tool = index
    i = 0
    for tool in self.tools:
      if i != self.current_tool:
        tool.widget().SetValue(False)
      i += 1
    self.tools[self.current_tool].widget().SetValue(True)

  def click(self, event):
    # event.GetEventObject() is the button that was pressed
    # .index is a custom defined property setup in Tool()
    self.set_tool(event.GetEventObject().index)

  def draw_cursor(self, ctx, cursor_x, cursor_y, canvas):
    if wx.GetKeyState(wx.WXK_CONTROL):
      self.tools[0].draw_cursor(ctx, cursor_x, cursor_y, self.tool_settings.get_size(), canvas)
    else:
      self.tools[self.current_tool].draw_cursor(ctx, cursor_x, cursor_y, self.tool_settings.get_size(), canvas)

  def widget(self):
      return self.box

def create(pnl, tileset, tool_settings):
  return Toolbar(pnl, tileset, tool_settings)

class Tool():
  def __init__(self, index, parent):
    self.button = wx.BitmapToggleButton(parent.box, label=wx.Bitmap(self.button_path))
    self.button.index = index
    self.button.Bind(wx.EVT_TOGGLEBUTTON, parent.click)

  def use(self, canvas, pixel_x, pixel_y, settings):
    pass

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    pass

  def widget(self):
    return self.button

  def draw_button(self, widget, ctx):
    self.button.draw_button(widget, ctx)

class Brush(Tool):
  def __init__(self, index, parent):
    self.index = index
    self.button_path = "./assets/pencil.png"
    Tool.__init__(self, index, parent)

  def use(self, canvas, pixel_x, pixel_y, settings):
    for x in range(int(pixel_x - settings.get_size() / 2 + 0.5), int(pixel_x + settings.get_size() / 2 + 0.5)):
      for y in range(int(pixel_y - settings.get_size() / 2 + 0.5), int(pixel_y + settings.get_size() / 2 + 0.5)):
        canvas.set_pixel(x, y, settings.get_color())

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    ctx.set_source_rgba(0.4, 0.8, 0.4, 1)
    ctx.rectangle(int(cursor_x - size / 2 + 0.5), int(cursor_y - size / 2 + 0.5), size, size)
    ctx.fill()

class ColorPicker(Tool):
  def __init__(self, index, parent):
    self.index = index
    self.button_path = "./assets/eye-dropper.png"
    Tool.__init__(self, index, parent)

  def use(self, canvas, pixel_x, pixel_y, settings):
    color = canvas.get_pixel(pixel_x, pixel_y)
    if color != None:
      settings.set_color(color)

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    ctx.set_source_rgba(0.4, 0.4, 1, 1)
    ctx.rectangle(int(cursor_x - size / 2 + 0.5), int(cursor_y - size / 2 + 0.5), size, size)
    ctx.fill()

class Eraser(Tool):
  def __init__(self, index, parent):
    self.index = index
    self.button_path = "./assets/eraser.png"
    self.radius = 1
    Tool.__init__(self, index, parent)

  def use(self, canvas, pixel_x, pixel_y, settings):
    canvas.set_pixel(pixel_x, pixel_y, gdk.Color(0, 0, 0))

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    ctx.set_source_rgba(1, 0.4, 0.4, 1)
    ctx.rectangle(int(cursor_x - size / 2 + 0.5), int(cursor_y - size / 2 + 0.5), size, size)
    ctx.fill()

class TilePlacer(Tool):
  def __init__(self, index, parent):
    self.index = index
    self.button_path = "./assets/box.png"
    self.radius = 1
    Tool.__init__(self, index, parent)

  def use(self, canvas, pixel_x, pixel_y, settings):
    canvas.place_tile(
        int(pixel_x / canvas.get_tileset().get_tile_width()),
        int(pixel_y / canvas.get_tileset().get_tile_height()),
        canvas.get_tileset().get_selected_tile())

  def draw_cursor(self, ctx, cursor_x, cursor_y, size, canvas):
    ctx.set_source_rgba(0.4, 0.4, 1, 1)
    x = int(cursor_x / canvas.get_tileset().get_tile_width())
    y = int(cursor_y / canvas.get_tileset().get_tile_height())
    ctx.rectangle(
        x * canvas.get_toolbar().get_tileset().tile_width,
        y * canvas.get_toolbar().get_tileset().tile_height,
        canvas.get_toolbar().get_tileset().tile_width,
        canvas.get_toolbar().get_tileset().tile_height)
    ctx.fill()
