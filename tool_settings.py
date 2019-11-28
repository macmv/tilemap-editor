import wx
import colorsys

class ToolSettings():
  def __init__(self, pnl):
    sizer = wx.GridBagSizer()
    self.box = wx.Panel(pnl) # main container for everything
    self.box.SetSizer(sizer)

    self.size_slider = wx.Slider(self.box, value=1, minValue=1, maxValue=10)

    self.color_gradient = wx.Panel(self.box)
    self.color_gradient.Bind(wx.EVT_PAINT, self.draw_sat)
    self.color_gradient.Bind(wx.EVT_SIZE, self.size_sat)
    self.color_gradient.Bind(wx.EVT_LEFT_DOWN, self.click_sat)
    self.color_gradient.Bind(wx.EVT_LEFT_UP, self.release_sat)
    self.color_gradient.Bind(wx.EVT_MOTION, self.move_sat)

    self.hue_gradient = wx.Panel(self.box)
    self.hue_gradient.Bind(wx.EVT_PAINT, self.draw_hue)
    # self.hue_gradient.Bind(wx.EVT_LEFT_DOWN, self.click_hue)
    # self.hue_gradient.Bind(wx.EVT_LEFT_UP, self.release_hue)
    # self.hue_gradient.Bind(wx.EVT_MOTION, self.move_hue)

    sizer.Add(self.size_slider,    pos=(0, 0), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=5)
    sizer.Add(self.color_gradient, pos=(1, 0), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
    sizer.Add(self.hue_gradient,   pos=(1, 1), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)

    sizer.AddGrowableCol(0)

    self.hue = 0 # 0 - 1
    self.sat = 1 # 0 - 1
    self.val = 1 # 0 - 1

  def size_sat(self, event):
    width = self.color_gradient.GetSize().GetWidth()
    self.color_gradient.SetSize((width, width))

  def draw_sat(self, event):
    width = self.color_gradient.GetSize().GetWidth()
    dc = wx.PaintDC(self.color_gradient)
    dc.DestroyClippingRegion()
    color = get_color(self.hue, 1, 1)
    for i in range(width):
      ratio = i / width
      dc.GradientFillLinear(
          wx.Rect(0, i, width, 1),
          tuple([ratio * j for j in (255, 255, 255)]),
          tuple([ratio * j for j in color]))
    dc.SetBrush(wx.Brush((0, 0, 0, 0)))
    dc.SetPen(wx.Pen((0, 0, 0, 255)))
    dc.DrawCircle(self.sat * width, self.val * width, width / 50)

  def draw_hue(self, event):
    width = self.color_gradient.GetSize().GetWidth()
    dc = wx.PaintDC(self.color_gradient)
    dc.DestroyClippingRegion()
    color = get_color(self.hue, 1, 1)
    for i in range(width):
      ratio = i / width
      dc.GradientFillLinear(
          wx.Rect(0, i, width, 1),
          tuple([ratio * j for j in (255, 255, 255)]),
          tuple([ratio * j for j in color]))
    dc.SetBrush(wx.Brush((0, 0, 0, 0)))
    dc.SetPen(wx.Pen((0, 0, 0, 255)))
    dc.DrawCircle(self.sat * width, self.val * width, width / 50)

  def click_sat(self, event):
    pass

  def release_sat(self, event):
    pass

  def move_sat(self, event):
    width = self.color_gradient.GetSize().GetWidth()
    self.sat = event.GetX() / width
    self.val = event.GetY() / width
    self.color_gradient.Refresh()

  def open_color_menu(self):
    self.color_button.clicked()

  def set_size(self, value):
    self.size_slider.set_value(value)

  def set_color(self, color):
    self.color_button.set_color(color)

  def get_color(self):
    return get_color(self.hue, self.sat, self.value)

  def get_size(self):
    return self.size_slider.GetValue()

  def widget(self):
    return self.box

def get_color(hue, sat, val):
  color = colorsys.hsv_to_rgb(hue, sat, val)
  return tuple([255 * i for i in color])

def create(pnl):
  return ToolSettings(pnl)
