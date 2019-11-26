import wx

class ToolSettings():
  def __init__(self, pnl):
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.box = wx.Panel(pnl) # main container for everything
    self.box.SetSizer(sizer)

    self.size_slider = wx.Slider(self.box, value=1, minValue=1, maxValue=10)
    sizer.Add(self.size_slider, 1, wx.EXPAND, 5)

    color_sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.color_picker = wx.Panel(self.box)
    self.color_picker.SetSizer(color_sizer)
    sizer.Add(self.color_picker, 1, wx.EXPAND, 5)

    self.color_gradient = wx.Panel(self.color_picker)
    color_sizer.Add(self.color_gradient, 1, wx.EXPAND, 5)
    self.color_gradient.Bind(wx.EVT_PAINT, self.draw)
    self.color_gradient.Bind(wx.EVT_SIZE, self.size)

  def size(self, event):
    width = self.color_gradient.GetSize().GetWidth()
    self.color_gradient.SetMinSize((width, width))

  def draw(self, event):
    width = self.color_gradient.GetSize().GetWidth()
    dc = wx.PaintDC(self.color_gradient)
    color = (255, 0, 0)
    for i in range(width):
      ratio = i / width
      dc.GradientFillLinear(
          wx.Rect(0, i, width, 1),
          tuple([ratio * j for j in (255, 255, 255)]),
          tuple([ratio * j for j in color]))

  def open_color_menu(self):
    self.color_button.clicked()

  def set_size(self, value):
    self.size_slider.set_value(value)

  def set_color(self, color):
    self.color_button.set_color(color)

  def get_color(self):
    return self.color_button.get_color()

  def get_size(self):
    return self.size_slider.GetValue()

  def widget(self):
    return self.box

def create(pnl):
  return ToolSettings(pnl)
