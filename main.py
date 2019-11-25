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

    left_sizer = wx.BoxSizer(wx.VERTICAL)
    left_pnl = wx.Panel(pnl)
    left_pnl.SetSizer(left_sizer)
    sizer.Add(left_pnl, 1, wx.LEFT, 5)

    center_sizer = wx.BoxSizer(wx.VERTICAL)
    center_pnl = wx.Panel(pnl)
    center_pnl.SetSizer(center_sizer)
    sizer.Add(center_pnl, 1, wx.CENTER|wx.EXPAND, 5)

    right_sizer = wx.BoxSizer(wx.VERTICAL)
    right_pnl = wx.Panel(pnl)
    right_pnl.SetSizer(right_sizer)
    sizer.Add(right_pnl, 1, wx.RIGHT, 5)

    tileset = tileset_module.create(right_pnl, 16, 16)
    tool_settings = tool_settings_module.create(left_pnl)
    toolbar = toolbar_module.create(left_pnl, tileset, tool_settings)
    canvas_manager = canvas_manager_module.create(center_pnl, toolbar)
    menu_bar = menu_bar_module.create(canvas_manager)

    self.SetMenuBar(menu_bar.widget())

    left_sizer.Add(toolbar.widget(), 1, 0, 5)
    left_sizer.Add(tool_settings.widget(), 1, 0, 5)
    center_sizer.Add(canvas_manager.widget(), 2, wx.EXPAND|wx.CENTER, 5)
    right_sizer.Add(tileset.widget(), 1, 0, 5)

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
