import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import menu_bar as menu_bar_module
import canvas_manager as canvas_manager_module
import toolbar as toolbar_module
import tool_settings as tool_settings_module
import tileset as tileset_module

class MyWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self)
    self.connect("destroy", gtk.main_quit)
    self.set_default_size(300, 250)
    settings = gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", True)

    header = gtk.HeaderBar(title="Tile Editor")
    header.props.show_close_button = True
    self.set_titlebar(header)

    self.grid = gtk.Grid()
    self.add(self.grid)

    tileset = tileset_module.create(16, 16)
    tool_settings = tool_settings_module.create(self)
    toolbar = toolbar_module.create(self, tileset, tool_settings)
    canvas_manager = canvas_manager_module.create(self, toolbar)
    menu_bar = menu_bar_module.create(self, canvas_manager)

    self.grid.attach(menu_bar.widget(), 0, 0, 5, 1)
    self.grid.attach(toolbar.widget(), 1, 1, 1, 1)
    self.grid.attach(tool_settings.widget(), 1, 2, 1, 2)
    self.grid.attach(canvas_manager.widget(), 2, 1, 2, 3)
    self.grid.attach(tileset.widget(), 4, 1, 1, 1)
    self.grid.attach(gtk.Button(label="Click Here"), 4, 2, 1, 2)

  def update_tileset(self, tileset):
    for widget in self.grid.get_children():
      if (self.grid.child_get_property(widget, "top_attach") == 1 and
          self.grid.child_get_property(widget, "left_attach") == 4):
        old_tileset = widget
        break
    self.grid.remove(old_tileset)
    self.grid.attach(tileset.widget(), 4, 1, 1, 1)

win = MyWindow()
win.show_all()
gtk.main()
