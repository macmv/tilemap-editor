import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk

class ToolSettings():
  def __init__(self):
    pass

  def widget(self):
    return gtk.Button(label="Click Here")

def create():
  return ToolSettings()
