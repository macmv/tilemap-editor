import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class MenuBar():
  def __init__(self):
    self.mb = gtk.MenuBar()

    self.mb.append(self.create_file())
    self.mb.append(self.create_edit())
    self.mb.append(self.create_tools())

  def widget(self):
    return self.mb

  def create_file(self):
    menu = gtk.Menu()
    new = gtk.ImageMenuItem(gtk.STOCK_NEW)
    menu.append(new)
    open = gtk.ImageMenuItem(gtk.STOCK_OPEN)
    menu.append(open)

    tab = gtk.MenuItem("File")
    tab.set_submenu(menu)
    return tab

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

def create():
  return MenuBar()
