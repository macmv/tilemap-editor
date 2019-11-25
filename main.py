import wx
import wx.grid as grid
import menu_bar as menu_bar_module
import canvas_manager as canvas_manager_module
import toolbar as toolbar_module
import tool_settings as tool_settings_module
import tileset as tileset_module

class TilemapFrame(wx.Frame):
  def __init__(self):
    super(TilemapFrame, self).__init__(None, title='Tilemap Editor')

    pnl = wx.Panel(self)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    pnl.SetSizer(sizer)
    tileset = tileset_module.create(pnl, 16, 16)
    toolbar = None
    canvas_manager = canvas_manager_module.create(pnl, toolbar)
    # tool_settings = tool_settings_module.create(pnl, self)
    # toolbar = toolbar_module.create(pnl, self, tileset, tool_settings)
    # menu_bar = menu_bar_module.create(pnl, self, canvas_manager)

    sizer.Add(canvas_manager.widget(), 2, wx.EXPAND|wx.CENTER, 5)
    sizer.Add(tileset.widget(), 1, 0, 5)
    # self.grid.attach(menu_bar.widget(), 0, 0, 5, 1)
    # self.grid.attach(toolbar.widget(), 1, 1, 1, 1)
    # self.grid.attach(tool_settings.widget(), 1, 2, 1, 2)
    # self.grid.attach(canvas_manager.widget(), 2, 1, 2, 3)
    # self.grid.attach(gtk.Button(label="Click Here"), 4, 2, 1, 2)

  def OnExit(self, event):
    self.Close(True)

  def update_tileset(self, tileset):
    old_tileset = None
    for widget in self.grid.get_children():
      if (self.grid.child_get_property(widget, "top_attach") == 1 and
          self.grid.child_get_property(widget, "left_attach") == 4):
        old_tileset = widget
        break
    if old_tileset != None:
      self.grid.remove(old_tileset)
    self.grid.attach(tileset.widget(), 4, 1, 1, 1)
    self.show_all()

if __name__ == '__main__':
  # When this module is run (not imported) then create the app, the
  # frame, show it, and start the event loop.
  app = wx.App()
  frm = TilemapFrame()
  frm.Show()
  app.MainLoop()
