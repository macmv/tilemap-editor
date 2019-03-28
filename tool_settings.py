import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk

class ToolSettings():
  def __init__(self, window):
    self.window = window
    self.size_slider = gtk.Scale.new_with_range(gtk.Orientation.HORIZONTAL, 1, 10, 1)
    self.size_slider.set_hexpand(True)
    self.grid = gtk.Grid()
    self.color_button = gtk.ColorButton()
    self.color_button.set_color(gdk.Color(0, 1, 0))
    self.grid.attach(self.size_slider, 0, 0, 5, 1)
    self.grid.attach(self.color_button, 0, 1, 1, 1)

  def set_size(self, value):
    self.size_slider.set_value(value)

  def set_color(self, color):
    self.color_button.set_color(color)

  def get_color(self):
    return self.color_button.get_color()

  def get_size(self):
    return self.size_slider.get_value()

  def widget(self):
    return self.grid

def create(window):
  return ToolSettings(window)
