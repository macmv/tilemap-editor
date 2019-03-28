import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class ToolSettings():
  def __init__(self):
    adj = gtk.Adjustment(10, 1, 100)
    self.size_slider = gtk.Scale(adjustment=adj)
    self.color_picker = gtk.ColorSelectionDialog()
    self.grid = gtk.Grid()
    self.grid.attach(self.size_slider, 0, 0, 1, 1)
    #self.grid.attach(self.color_picker, 0, 1, 1, 1)

  def get_color(self):
    return (1, 1, 0, 1)
    
  def get_size(self):
    return self.size_slider.get_value()

  def widget(self):
    return self.grid

def create():
  return ToolSettings()
