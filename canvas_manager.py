import wx
import canvas as canvas_module
import toolbar as toolbar_module
import tileset as tileset_module
import tool_settings as tool_settings_module

class CanvasManager:
  def __init__(self, pnl, window, toolbar):
    buttons = [
            wx.Button(pnl, label="ONE"),
            wx.Button(pnl, label="TWO"),
            wx.Button(pnl, label="TREE")]

    self.pnl = wx.Panel(pnl)
    self.pnl.Bind(wx.EVT_PAINT, self.onPaint)
    self.pnl.SetBackgroundColour("#E6E6E6")

    sizer = wx.BoxSizer(wx.VERTICAL)
    for btn in buttons:
      sizer.Add(btn, 0, wx.ALL, 5)
    sizer.Add(self.pnl, 1, wx.EXPAND|wx.ALL, 5)
    pnl.SetSizer(sizer)

    # self.add(self.grid)

    # self.window = window
    # self.toolbar = toolbar
    # self.tool_settings = tool_settings_module.create(window)
    # self.canvases = []
    # self.current_canvas = -1
    # self.da = gtk.DrawingArea()
    # self.da.set_size_request(960, 540) # 0.5 * 1080p
    # self.da.set_hexpand(True)
    # self.da.set_vexpand(True)
    # self.da.connect("draw", self.draw)
    # window.connect("key-press-event", self.key_press)
    # window.connect("key-release-event", self.key_release)
    # self.event_box = gtk.EventBox()
    # self.event_box.connect("button-press-event", self.click)
    # self.event_box.connect("button-release-event", self.release)
    # self.event_box.connect("motion-notify-event", self.move)
    # self.event_box.connect("scroll-event", self.scroll)
    # self.event_box.add_events(
    #     gdk.EventMask.BUTTON_PRESS_MASK
    #   | gdk.EventMask.BUTTON_RELEASE_MASK
    #   | gdk.EventMask.POINTER_MOTION_MASK
    #   | gdk.EventMask.SCROLL_MASK)
    # self.event_box.add(self.da)

    # self.tab_switcher = gtk.Box(orientation=gtk.Orientation.HORIZONTAL)
    # self.tab_switcher.show()

    # self.box = gtk.Box(orientation=gtk.Orientation.VERTICAL)
    # self.box.pack_start(self.tab_switcher, False, False, 0)
    # self.box.pack_start(self.event_box, True, True, 0)
    # self.box.show()

    # self.new(None)

  def onPaint(self, event):
    dc = wx.PaintDC(self.pnl)
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

  def get_current_canvas(self):
    return self.canvases[self.current_canvas]

  def draw(self, widget, ctx):
    if self.canvases:
      self.canvases[self.current_canvas].draw(widget, ctx)

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

def create(pnl, window, toolbar):
  return CanvasManager(pnl, window, toolbar)
