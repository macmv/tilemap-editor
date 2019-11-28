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
    self.sizer = wx.GridBagSizer()
    self.pnl.SetSizer(self.sizer)

    tileset = tileset_module.create(self.pnl, 16, 16)
    tool_settings = tool_settings_module.create(self.pnl)
    toolbar = toolbar_module.create(self.pnl, tileset, tool_settings)
    canvas_manager = canvas_manager_module.create(self.pnl, self, toolbar)
    menu_bar = menu_bar_module.create(canvas_manager)

    self.SetMenuBar(menu_bar.widget())

    self.sizer.Add(toolbar.widget(),        pos=(0, 0), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
    self.sizer.Add(tool_settings.widget(),  pos=(1, 0), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
    self.sizer.Add(canvas_manager.widget(), pos=(0, 1), span=(2, 1), flag=wx.EXPAND|wx.ALL, border=5)
    self.sizer.Add(tileset.widget(),        pos=(0, 2), span=(2, 1), flag=wx.EXPAND|wx.ALL, border=5)

    self.sizer.AddGrowableCol(1)
    self.sizer.AddGrowableRow(1)

  def create_tileset(self):
    tileset = tileset_module.create(self.pnl, 16, 16)
    return tileset

  def OnExit(self, event):
    self.Close(True)

  def update_tileset(self, tileset):
    old_tileset = self.pnl.GetChildren()[3]
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
