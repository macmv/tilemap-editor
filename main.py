import wx
import wx.grid as grid
import menu_bar as menu_bar_module
import canvas_manager as canvas_manager_module
import toolbar as toolbar_module
import tool_settings as tool_settings_module
import tileset as tileset_module
import wx.lib.inspection

class TilemapFrame(wx.Frame):
  def __init__(self):
    super(TilemapFrame, self).__init__(None, title='Tilemap Editor')

    self.pnl = wx.Panel(self)
    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.pnl.SetSizer(self.sizer)

    self.left_sizer = wx.BoxSizer(wx.VERTICAL)
    self.left_pnl = wx.Panel(self.pnl)
    self.left_pnl.SetSizer(self.left_sizer)
    self.sizer.Add(self.left_pnl, 1, wx.LEFT, 5) # 1/8 of width

    self.center_sizer = wx.BoxSizer(wx.VERTICAL)
    self.center_pnl = wx.Panel(self.pnl)
    self.center_pnl.SetSizer(self.center_sizer)
    self.sizer.Add(self.center_pnl, 6, wx.CENTER|wx.EXPAND, 5) # 6/8 of width

    self.right_sizer = wx.BoxSizer(wx.VERTICAL)
    self.right_pnl = wx.Panel(self.pnl)
    self.right_pnl.SetSizer(self.right_sizer)
    self.sizer.Add(self.right_pnl, 1, wx.RIGHT, 5) # 1/8 of width

    tileset = tileset_module.create(self.right_pnl, 16, 16)
    tool_settings = tool_settings_module.create(self.left_pnl)
    toolbar = toolbar_module.create(self.left_pnl, tileset, tool_settings)
    canvas_manager = canvas_manager_module.create(self.center_pnl, self, toolbar)
    menu_bar = menu_bar_module.create(canvas_manager)

    self.SetMenuBar(menu_bar.widget())

    self.left_sizer.Add(toolbar.widget(), 1, wx.EXPAND, 5)
    self.left_sizer.Add(tool_settings.widget(), 1, wx.EXPAND, 5)
    self.center_sizer.Add(canvas_manager.widget(), 2, wx.EXPAND, 5)
    self.right_sizer.Add(tileset.widget(), 1, wx.EXPAND, 5)

  def create_tileset(self):
    tileset = tileset_module.create(self.right_pnl, 16, 16)
    return tileset

  def OnExit(self, event):
    self.Close(True)

  def update_tileset(self, tileset):
    old_tileset = self.right_pnl.GetChildren()[1]
    print(tileset.widget())
    print(old_tileset)
    # self.right_sizer.Detach(old_tileset)
    # old_tileset.Destroy()
    # self.right_sizer.Add(tileset.widget(), 1, 0, 5)

if __name__ == '__main__':
  # When this module is run (not imported) then create the app, the
  # frame, show it, and start the event loop.
  app = wx.App()
  frm = TilemapFrame()
  frm.Show()
  # enable debugging \/
  # wx.lib.inspection.InspectionTool().Show()
  app.MainLoop()
