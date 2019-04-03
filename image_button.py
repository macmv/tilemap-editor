import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import cairo

class Button:
  def __init__(self, filename):
    self.button_surface = cairo.ImageSurface.create_from_png(filename)
    self.button_pattern = cairo.SurfacePattern(self.button_surface)
    self.button = gtk.Button()
    self.button.set_size_request(32, 32 * 1.35)
    da = gtk.DrawingArea()
    da.connect("draw", self.draw_button)
    self.button.add(da)
    da.show()
    self.button.show()

  def widget(self):
    return self.button

  def draw_button(self, widget, ctx):
    ctx.scale(widget.get_allocated_width() / self.button_surface.get_width(),
        widget.get_allocated_height() / self.button_surface.get_height())
    ctx.set_source(self.button_pattern)
    ctx.paint()
