import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import file_manager

class MenuBar():
  def __init__(self, window, canvas_manager):
    self.window = window
    self.canvas_manager = canvas_manager

    self.mb = gtk.MenuBar()
    self.mb.append(self.create_file())
    self.mb.append(self.create_edit())
    self.mb.append(self.create_tools())

  def widget(self):
    return self.mb

  def create_file(self):
    menu = gtk.Menu()
    new = gtk.ImageMenuItem(gtk.STOCK_NEW)
    new.connect("activate", self.new_canvas)
    menu.append(new)
    open = gtk.ImageMenuItem(gtk.STOCK_OPEN)
    open.connect("activate", self.open_file)
    menu.append(open)
    save = gtk.ImageMenuItem(gtk.STOCK_SAVE)
    save.connect("activate", self.save_file)
    menu.append(save)

    tab = gtk.MenuItem("File")
    tab.set_submenu(menu)
    return tab

  def new_canvas(self, widget):
    dialog = NewDialog(self.window)
    r = dialog.run()
    dialog.close()
    if r == gtk.ResponseType.OK:
      print("Creating new canvas")
      self.canvas_manager.new(dialog)

  def open_file(self, widget):
    # TODO: add gui here
    self.canvas_manager.open("test")

  def save_file(self, widget):
    # TODO: add gui here
    self.canvas_manager.save("test")

  def create_edit(self):
    menu = gtk.Menu()
    copy = gtk.ImageMenuItem(gtk.STOCK_COPY)
    menu.append(copy)
    cut = gtk.ImageMenuItem(gtk.STOCK_CUT)
    menu.append(cut)
    paste = gtk.ImageMenuItem(gtk.STOCK_PASTE)
    menu.append(paste)

    tab = gtk.MenuItem("Edit")
    tab.set_submenu(menu)
    return tab

  def create_tools(self):
    menu = gtk.Menu()
    copy = gtk.ImageMenuItem(gtk.STOCK_COPY)
    menu.append(copy)

    tab = gtk.MenuItem("Tools")
    tab.set_submenu(menu)
    return tab

class NewDialog(gtk.Dialog):
  def __init__(self, parent):
    gtk.Dialog.__init__(self, "", parent, 0,
        (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
         gtk.STOCK_OK, gtk.ResponseType.OK))

    header = gtk.HeaderBar(title="New File")
    header.props.show_close_button = True
    self.set_titlebar(header)

    self.set_default_size(150, 100)

    label = gtk.Label("This is a dialog to display additional information")

    box = self.get_content_area()
    box.add(label)
    self.show_all()

def create(window, canvas):
  return MenuBar(window, canvas)
