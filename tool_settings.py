import wx

class ToolSettings():
  def __init__(self, pnl):
    sizer = wx.BoxSizer(wx.VERTICAL)
    self.box = wx.Panel(pnl) # main container for everything
    self.box.SetSizer(sizer)

    self.size_slider = wx.Slider(self.box, value=1, minValue=1, maxValue=10)
    sizer.Add(self.size_slider, 1, wx.EXPAND, 5)

    self.color_button = wx.Button(self.box)
    sizer.Add(self.color_button, 1, 0, 5)

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
