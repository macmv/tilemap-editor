import wx
import canvas as canvas_module
import toolbar as toolbar_module
import tileset as tileset_module
import tool_settings as tool_settings_module

class CanvasManager:
  def __init__(self, pnl, toolbar):
    self.box = wx.Panel(pnl)
    box_sizer = wx.BoxSizer(wx.VERTICAL)
    self.box.SetSizer(box_sizer)

    self.tab_switcher = wx.Panel(self.box)
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
    self.da.Bind(wx.EVT_MOTION, self.move)

  def draw(self, event):
    dc = wx.PaintDC(self.da)
    dc.SetPen(wx.Pen('#d4d4d4'))

    dc.SetBrush(wx.Brush('#c56c00'))
    dc.DrawRectangle(10, 15, 90, 60)

    dc.SetBrush(wx.Brush('#1ac500'))
    dc.DrawRectangle(130, 15, 90, 60)

    dc.SetBrush(wx.Brush('#539e47'))
    dc.DrawRectangle(250, 15, 90, 60)

    dc.SetBrush(wx.Brush('#004fc5'))
    dc.DrawRectangle(10, 105, 90, 60)

    dc.SetBrush(wx.Brush('#c50024'))
    dc.DrawRectangle(130, 105, 90, 60)

    dc.SetBrush(wx.Brush('#9e4757'))
    dc.DrawRectangle(250, 105, 90, 60)

    dc.SetBrush(wx.Brush('#5f3b00'))
    dc.DrawRectangle(10, 195, 90, 60)

    dc.SetBrush(wx.Brush('#4c4c4c'))
    dc.DrawRectangle(130, 195, 90, 60)

    dc.SetBrush(wx.Brush('#785f36'))
    dc.DrawRectangle(250, 195, 90, 60)
    if self.canvases:
      self.canvases[self.current_canvas].draw(widget, ctx)

  def get_current_canvas(self):
    return self.canvases[self.current_canvas]

  def click(self, widget, event):
    if self.canvases:
      self.canvases[self.current_canvas].click(widget, event)

  def release(self, widget, event):
    if self.canvases:
      self.canvases[self.current_canvas].release(widget, event)

  def move(self, widget, event):
    if self.canvases:
      self.canvases[self.current_canvas].move(widget, event)

  def scroll(self, widget, event):
    if self.canvases:
      self.canvases[self.current_canvas].scroll(widget, event)

  def key_press(self, widget, event):
    if self.canvases:
      self.canvases[self.current_canvas].key_press(widget, event)

  def key_release(self, widget, event):
    if self.canvases:
      self.canvases[self.current_canvas].key_release(widget, event)

  def widget(self):
    return self.box

  def open(self, filename):
    canvas = canvas_module.load_from_file(filename, self.window, self.toolbar)
    self.canvases.append(canvas)
    self.add_tab()

  def save(self, filename):
    if self.canvases:
      self.canvases[self.current_canvas].save(filename)

  def new(self, dialog):
    tileset = tileset_module.create(16, 16)
    self.toolbar.set_tileset(tileset)
    canvas = canvas_module.load_from_settings(5, 5, self.window, self.toolbar)
    self.canvases.append(canvas)
    self.window.update_tileset(tileset)
    self.add_tab()

  def add_tab(self):
    button = gtk.Button()
    button.connect("clicked", self.set_canvas)
    button.id = len(self.canvases) - 1
    button.show()
    self.tab_switcher.pack_start(button, False, False, 0)

  def set_canvas(self, widget):
    self.current_canvas = widget.id
    canvas = self.canvases[self.current_canvas]
    self.window.update_tileset(canvas.tileset)

def create(pnl, toolbar):
  return CanvasManager(pnl, toolbar)
