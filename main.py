import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import menu_bar as menu_bar_module
import canvas as canvas_module
import toolbar as toolbar_module
import tool_settings as tool_settings_module
import tileset as tileset_module

class MyWindow(gtk.Window):
  def __init__(self):
    gtk.Window.__init__(self, title="Hello World")
    self.connect("destroy", gtk.main_quit)
    self.set_default_size(300, 250)

    header = gtk.HeaderBar(title="Tile Editor")
    header.props.show_close_button = True
    self.set_titlebar(header)

    grid = gtk.Grid()
    self.add(grid)

    menu_bar = menu_bar_module.create()
    tileset = tileset_module.create()
    tool_settings = tool_settings_module.create(self)
    toolbar = toolbar_module.create(self, tileset, tool_settings)
    canvas = canvas_module.create(self, toolbar)

    grid.attach(menu_bar.widget(), 0, 0, 5, 1)
    grid.attach(toolbar.widget(), 1, 1, 1, 1)
    grid.attach(tool_settings.widget(), 1, 2, 1, 2)
    grid.attach(canvas.widget(), 2, 1, 2, 3)
    grid.attach(gtk.Button(label="Click Here"), 4, 1, 1, 1)
    grid.attach(gtk.Button(label="Click Here"), 4, 2, 1, 2)

win = MyWindow()
win.show_all()
gtk.main()
