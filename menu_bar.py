import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
import file_manager

class MenuBar():
  def __init__(self, canvas):
    self.mb = gtk.MenuBar()

    self.mb.append(self.create_file(canvas))
    self.mb.append(self.create_edit())
    self.mb.append(self.create_tools())

  def widget(self):
    return self.mb

  def create_file(self, canvas):
    self.fm = file_manager.FileManager(canvas)
    menu = gtk.Menu()
    new = gtk.ImageMenuItem(gtk.STOCK_NEW)
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

  def save_file(self, widget):
    # TODO: add gui here
    self.fm.save("test")

  def open_file(self, widget):
    # TODO: add gui here
    self.fm.open("test")

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

def create(canvas):
  return MenuBar(canvas)
