import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import canvas as canvas_module
import toolbar as toolbar_module
import tileset as tileset_module
import tool_settings as tool_settings_module

class CanvasManager:
  def __init__(self, window, toolbar):
    self.window = window
    self.toolbar = toolbar
    self.tool_settings = tool_settings_module.create(window)
    self.canvases = []
    self.current_canvas = -1
    self.da = gtk.DrawingArea()
    self.da.set_size_request(960, 540) # 0.5 * 1080p
    self.da.set_hexpand(True)
    self.da.set_vexpand(True)
    self.da.connect("draw", self.draw)
    window.connect("key-press-event", self.key_press)
    window.connect("key-release-event", self.key_release)
    self.event_box = gtk.EventBox()
    self.event_box.connect("button-press-event", self.click)
    self.event_box.connect("button-release-event", self.release)
    self.event_box.connect("motion-notify-event", self.move)
    self.event_box.connect("scroll-event", self.scroll)
    self.event_box.add_events(
        gdk.EventMask.BUTTON_PRESS_MASK
      | gdk.EventMask.BUTTON_RELEASE_MASK
      | gdk.EventMask.POINTER_MOTION_MASK
      | gdk.EventMask.SCROLL_MASK)
    self.event_box.add(self.da)

    self.tab_switcher = gtk.Box(orientation=gtk.Orientation.HORIZONTAL)
    self.tab_switcher.show()

    self.box = gtk.Box(orientation=gtk.Orientation.VERTICAL)
    self.box.pack_start(self.tab_switcher, False, False, 0)
    self.box.pack_start(self.event_box, True, True, 0)
    self.box.show()

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
    self.tab_switcher.pack_start(button, False, False, 0)

  def set_canvas(self, widget):
    self.current_canvas = widget.id
    canvas = self.canvases[self.current_canvas]
    self.window.update_tileset(canvas.tileset)

def create(window, toolbar):
  return CanvasManager(window, toolbar)
