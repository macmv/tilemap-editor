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

    header = gtk.HeaderBar(title="Tile Editor")
    header.props.show_close_button = True
    self.set_titlebar(header)

    grid = gtk.Grid()
    self.add(grid)

    tileset = tileset_module.create(16, 16)
    tool_settings = tool_settings_module.create(self)
    toolbar = toolbar_module.create(self, tileset, tool_settings)
    canvas_manager = canvas_manager_module.create(self, toolbar)
    menu_bar = menu_bar_module.create(self, canvas_manager)

    grid.attach(menu_bar.widget(), 0, 0, 5, 1)
    grid.attach(toolbar.widget(), 1, 1, 1, 1)
    grid.attach(tool_settings.widget(), 1, 2, 1, 2)
    grid.attach(canvas_manager.widget(), 2, 1, 2, 3)
    grid.attach(tileset.widget(), 4, 1, 1, 1)
    grid.attach(gtk.Button(label="Click Here"), 4, 2, 1, 2)

win = MyWindow()
win.show_all()
gtk.main()
