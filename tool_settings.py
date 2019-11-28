import wx
import colorsys

class ToolSettings():
  def __init__(self, pnl):
    sizer = wx.GridBagSizer()
    self.box = wx.Panel(pnl) # main container for everything
    self.box.SetSizer(sizer)

    self.size_slider = wx.Slider(self.box, value=1, minValue=1, maxValue=10)

    self.color_gradient = FixedPanel(self.box, 1, 1)
    self.color_gradient.Bind(wx.EVT_PAINT, self.draw_sat)
    self.color_gradient.Bind(wx.EVT_SIZE, self.size_sat)
    self.color_gradient.Bind(wx.EVT_LEFT_DOWN, self.click)
    self.color_gradient.Bind(wx.EVT_LEFT_UP, self.release)
    self.color_gradient.Bind(wx.EVT_MOTION, self.move_sat)

    self.hue_gradient = wx.Panel(self.box)
    self.hue_gradient.Bind(wx.EVT_PAINT, self.draw_hue)
    self.hue_gradient.Bind(wx.EVT_LEFT_DOWN, self.click)
    self.hue_gradient.Bind(wx.EVT_LEFT_UP, self.release)
    self.hue_gradient.Bind(wx.EVT_MOTION, self.move_hue)

    column_sizer = wx.GridBagSizer()
    self.column_box = wx.Panel(self.box) # for hue, sat, value, and current color columns
    self.column_box.SetSizer(column_sizer)

    self.hue_picker = ColorPicker(self, 0.1, 0, 0)
    self.sat_picker = ColorPicker(self, 0, 0.2, 0)
    self.val_picker = ColorPicker(self, 0, 0, 0.2)

    sizer.Add(self.size_slider,                pos=(0, 0), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
    sizer.Add(self.color_gradient,             pos=(1, 0), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
    sizer.Add(self.hue_gradient,               pos=(1, 1), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
    sizer.Add(self.column_box,                 pos=(2, 0), span=(1, 2), flag=wx.EXPAND|wx.ALL, border=5)
    column_sizer.Add(self.hue_picker.widget(), pos=(0, 0), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
    column_sizer.Add(self.sat_picker.widget(), pos=(0, 1), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
    column_sizer.Add(self.val_picker.widget(), pos=(0, 2), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)

    sizer.AddGrowableCol(0)
    sizer.AddGrowableCol(1)
    sizer.AddGrowableRow(2)
    column_sizer.AddGrowableRow(0)
    column_sizer.AddGrowableCol(0)
    column_sizer.AddGrowableCol(1)
    column_sizer.AddGrowableCol(2)

    self.hue = 0 # 0 - 1
    self.sat = 1 # 0 - 1
    self.val = 1 # 0 - 1

    self.mouse_down = False

    self.size_sat_count = 0

  def size_sat(self, event):
    if self.size_sat_count < 5:
      self.color_gradient.InvalidateBestSize()
      self.size_sat_count += 1

  def draw_sat(self, event):
    width = self.color_gradient.GetSize().GetWidth()
    dc = wx.PaintDC(self.color_gradient)
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
    width = self.hue_gradient.GetSize().GetWidth()
    height = self.hue_gradient.GetSize().GetHeight()
    dc = wx.PaintDC(self.hue_gradient)
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    dc.GradientFillLinear(
        wx.Rect(0, height * 0 / 3, width, height / 3),
        colors[0],
        colors[1],
        wx.DOWN)
    dc.GradientFillLinear(
        wx.Rect(0, height * 1 / 3, width, height / 3),
        colors[1],
        colors[2],
        wx.DOWN)
    dc.GradientFillLinear(
        wx.Rect(0, height * 2 / 3, width, height / 3),
        colors[2],
        colors[0],
        wx.DOWN)
    dc.SetPen(wx.Pen((0, 0, 0, 255)))
    dc.DrawLine(0, self.hue * height, width, self.hue * height)
    dc.SetPen(wx.Pen((255, 255, 255, 255)))
    dc.DrawLine(0, self.hue * height - 1, width, self.hue * height - 1)
    dc.DrawLine(0, self.hue * height + 1, width, self.hue * height + 1)

  def click(self, event):
    self.mouse_down = True

  def release(self, event):
    self.mouse_down = False

  def move_sat(self, event):
    if self.mouse_down:
      width = self.color_gradient.GetSize().GetWidth()
      self.sat = event.GetX() / width
      self.val = event.GetY() / width
      self.color_gradient.Refresh()
      self.hue_picker.refresh()
      self.sat_picker.refresh()
      self.val_picker.refresh()

  def move_hue(self, event):
    if self.mouse_down:
      height = self.hue_gradient.GetSize().GetHeight()
      self.hue = event.GetY() / height
      self.hue_gradient.Refresh()
      self.color_gradient.Refresh()
      self.hue_picker.refresh()
      self.sat_picker.refresh()
      self.val_picker.refresh()

  def open_color_menu(self):
    self.color_button.clicked()

  def set_size(self, value):
    self.size_slider.set_value(value)

  def set_color(self, color):
    self.color_button.set_color(color)

  def get_color(self):
    return get_color(self.hue, self.sat, self.val)

  def get_size(self):
    return self.size_slider.GetValue()

  def widget(self):
    return self.box

def get_color(hue, sat, val):
  color = colorsys.hsv_to_rgb(hue, sat, val)
  return tuple([255 * i for i in color])

def create(pnl):
  return ToolSettings(pnl)

class FixedPanel(wx.Panel):
  def __init__(self, parent, wratio, hratio):
    wx.Panel.__init__(self, parent)
    self.wratio = wratio
    self.hratio = hratio

  def DoGetBestSize(self):
    width = self.GetSize().GetWidth()
    return (width * self.wratio, width * self.hratio)

class ColorPicker():
  def __init__(self, settings, hue_offset, sat_offset, val_offset):
    self.parent = settings
    self.gradient = FixedPanel(settings.column_box, 1, 1)
    self.gradient.Bind(wx.EVT_PAINT, self.draw)
    self.gradient.Bind(wx.EVT_SIZE, self.size)
    self.selected = 0
    self.hue_offset = hue_offset
    self.sat_offset = sat_offset
    self.val_offset = val_offset

  def size(self, event):
    width = self.gradient.GetSize().GetWidth()
    self.gradient.SetSize((width, width * 2))

  def refresh(self):
    self.gradient.Refresh()

  def draw(self, event):
    width = self.gradient.GetSize().GetWidth()
    height = self.gradient.GetSize().GetHeight()
    dc = wx.PaintDC(self.gradient)
    color = self.parent.get_color()
    hue = self.parent.hue
    sat = self.parent.sat
    val = self.parent.val
    for i in range(5):
      new_hue = hue + self.hue_offset * (i - 2)
      new_sat = sat + self.sat_offset * (i - 2)
      new_val = val + self.val_offset * (i - 2)
      if new_hue > 1:
        new_hue -= 1
      if new_hue < 0:
        new_hue += 1
      new_sat = max(min(new_sat, 1), 0)
      new_val = max(min(new_val, 1), 0)
      color = get_color(new_hue, new_sat, new_val)
      if i == 2:
        dc.SetPen(wx.Pen((255, 255, 255)))
      else:
        dc.SetPen(wx.Pen(color))
      dc.SetBrush(wx.Brush(color))
      dc.DrawRectangle(wx.Rect(0, height * i / 5, width, height / 5 + 1))

  def widget(self):
    return self.gradient
