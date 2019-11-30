import wx
import wx.lib.wxcairo
import canvas as canvas_module
import toolbar as toolbar_module
import tileset as tileset_module
import tool_settings as tool_settings_module

class CanvasManager:
  def __init__(self, pnl, window, toolbar):
    self.window = window
    self.box = wx.Panel(pnl)
    box_sizer = wx.BoxSizer(wx.VERTICAL)
    self.box.SetSizer(box_sizer)

    self.tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.tab_switcher = wx.Panel(self.box)
    self.tab_switcher.SetSizer(self.tab_sizer)
    box_sizer.Add(self.tab_switcher, 0, wx.ALL, 5)

    self.toolbar = toolbar
    self.tool_settings = toolbar.tool_settings
    self.canvases = []
    self.current_canvas = -1
    self.da = wx.Panel(self.box)
    box_sizer.Add(self.da, 1, wx.EXPAND|wx.ALL, 5)
    self.da.Bind(wx.EVT_PAINT, self.draw)
    self.da.Bind(wx.EVT_LEFT_DOWN, self.click)
    self.da.Bind(wx.EVT_LEFT_UP, self.release)
    self.da.Bind(wx.EVT_MIDDLE_DOWN, self.click)
    self.da.Bind(wx.EVT_MIDDLE_UP, self.release)
    self.da.Bind(wx.EVT_MOUSEWHEEL, self.scroll)
    self.da.Bind(wx.EVT_MOTION, self.move)
    window.Bind(wx.EVT_CHAR_HOOK, self.key_press)

  def draw(self, event):
    dc = wx.PaintDC(self.da)
    ctx = wx.lib.wxcairo.ContextFromDC(dc)
    if self.canvases:
      self.canvases[self.current_canvas].draw(ctx)

  def get_current_canvas(self):
    return self.canvases[self.current_canvas]

  def click(self, event):
    if self.canvases:
      self.canvases[self.current_canvas].click(event)

  def release(self, event):
    if self.canvases:
      self.canvases[self.current_canvas].release(event)

  def move(self, event):
    if self.canvases:
      self.canvases[self.current_canvas].move(event)
      self.da.Refresh()

  def scroll(self, event):
    if self.canvases:
      self.canvases[self.current_canvas].scroll(event)
      self.da.Refresh()

  def key_press(self, event):
    if self.canvases:
      self.canvases[self.current_canvas].key_press(event)
      self.da.Refresh()

  def widget(self):
    return self.box

  def open(self, filename):
    canvas = canvas_module.load_from_file(filename, self.window, self.toolbar)
    self.canvases.append(canvas)
    self.add_tab()

  def save(self, filename):
    if self.canvases:
      self.canvases[self.current_canvas].save(filename)

  def new(self, width, height, tile_width, tile_height):
    tileset = self.window.create_tileset(tile_width, tile_height)
    self.toolbar.set_tileset(tileset)
    canvas = canvas_module.load_from_settings(width, height, self.window, self.toolbar)
    self.canvases.append(canvas)
    self.window.update_tileset(tileset)
    self.add_tab()

  def add_tab(self):
    button = wx.Button(self.tab_switcher)
    button.Bind(wx.EVT_BUTTON, self.set_canvas)
    button.id = len(self.canvases) - 1
    self.tab_sizer.Add(button, 1, wx.EXPAND|wx.ALL, 5)
    self.box.Layout()

  def set_canvas(self, event):
    widget = event.GetEventObject()
    self.current_canvas = widget.id
    canvas = self.canvases[self.current_canvas]
    self.toolbar.set_tileset(canvas.tileset)
    self.window.update_tileset(canvas.tileset)

def create(pnl, window, toolbar):
  return CanvasManager(pnl, window, toolbar)
