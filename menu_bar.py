import wx
import file_manager

class MenuBar():
  def __init__(self, canvas_manager, window):
    self.canvas_manager = canvas_manager

    self.window = window

    self.mb = wx.MenuBar()
    self.mb.Append(self.create_file(), "File")
    # self.mb.Append(self.create_edit())
    # self.mb.Append(self.create_tools())

  def widget(self):
    return self.mb

  # is the file tab in the menu
  def create_file(self):
    menu = wx.Menu()

    new = wx.MenuItem(menu, wx.ID_NEW, "New")
    menu.Bind(wx.EVT_MENU, self.new_file, new)
    menu.Append(new)

    open_ = wx.MenuItem(menu, wx.ID_OPEN, "Open")
    menu.Bind(wx.EVT_MENU, self.open_file, open_)
    menu.Append(open_)

    save = wx.MenuItem(menu, wx.ID_SAVE, "Save")
    menu.Bind(wx.EVT_MENU, self.save_file, save)
    menu.Append(save)

    saveas = wx.MenuItem(menu, wx.ID_SAVEAS, "Save As")
    menu.Bind(wx.EVT_MENU, self.save_as, saveas)
    menu.Append(saveas)

    return menu

  # is the edit tab in the menu
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

  # is the tools tab in the menu
  def create_tools(self):
    menu = gtk.Menu()
    copy = gtk.ImageMenuItem(gtk.STOCK_COPY)
    menu.append(copy)

    tab = gtk.MenuItem("Tools")
    tab.set_submenu(menu)
    return tab

  def new_file(self, event):
    dialog = NewDialog(self.window)
    status = dialog.ShowModal()
    if status == wx.ID_OK:
      self.canvas_manager.new(dialog)

  def open_file(self, widget):
    dialog = gtk.FileChooserDialog("Choose a file", None,
      gtk.FileChooserAction.OPEN,
      (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
       gtk.STOCK_OPEN, gtk.ResponseType.OK))
    filter_text = gtk.FileFilter()
    filter_text.set_name("Map files")
    filter_text.add_pattern("*.map")
    dialog.add_filter(filter_text)

    response = dialog.run()
    dialog.close()

    if response == gtk.ResponseType.OK:
      self.canvas_manager.open(dialog.get_filename())

  def save_file(self, widget):
    dialog = gtk.FileChooserDialog("Please choose where to save", None,
      gtk.FileChooserAction.SAVE,
      (gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
       gtk.STOCK_SAVE, gtk.ResponseType.OK))
    filter_text = gtk.FileFilter()
    filter_text.set_name("Map files")
    filter_text.add_pattern("*.map")
    dialog.add_filter(filter_text)

    response = dialog.run()
    dialog.close()

    if response == gtk.ResponseType.OK:
      filename = dialog.get_filename()
      if not '.' in filename:
        filename = filename + ".map"
      self.canvas_manager.save(filename)

  def save_as(self, event):
    pass

class NewDialog(wx.Dialog):
  def __init__(self, parent):
    super(NewDialog, self).__init__(parent, title="New File", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

    sizer = wx.GridBagSizer()
    pnl = wx.Panel(self)
    pnl.SetSizer(sizer)

    width_text        = wx.StaticText(pnl, label="Map Width:")
    width_entry       = wx.SpinCtrl(pnl)
    height_text       = wx.StaticText(pnl, label="Map Height:")
    height_entry      = wx.SpinCtrl(pnl)
    tile_width_text   = wx.StaticText(pnl, label="Tile Width:")
    tile_width_entry  = wx.SpinCtrl(pnl)
    tile_height_text  = wx.StaticText(pnl, label="Tile Height:")
    tile_height_entry = wx.SpinCtrl(pnl)
    cancel_button     = wx.Button(pnl, label="Cancel")
    ok_button         = wx.Button(pnl, label="Ok")

    sizer.Add(width_text,        pos=(1, 0), span=(1, 1), flag=wx.ALL,                border=5)
    sizer.Add(width_entry,       pos=(1, 1), span=(1, 2), flag=wx.ALL,                border=5)
    sizer.Add(height_text,       pos=(2, 0), span=(1, 1), flag=wx.ALL,                border=5)
    sizer.Add(height_entry,      pos=(2, 1), span=(1, 2), flag=wx.ALL,                border=5)
    sizer.Add(tile_width_text,   pos=(3, 0), span=(1, 1), flag=wx.ALL,                border=5)
    sizer.Add(tile_width_entry,  pos=(3, 1), span=(1, 2), flag=wx.ALL,                border=5)
    sizer.Add(tile_height_text,  pos=(4, 0), span=(1, 1), flag=wx.ALL,                border=5)
    sizer.Add(tile_height_entry, pos=(4, 1), span=(1, 2), flag=wx.ALL,                border=5)
    sizer.Add(cancel_button,     pos=(5, 1), span=(1, 1), flag=wx.ALL|wx.ALIGN_RIGHT, border=5)
    sizer.Add(ok_button,         pos=(5, 2), span=(1, 1), flag=wx.ALL|wx.ALIGN_RIGHT, border=5)

    sizer.AddGrowableCol(0)

    self.SetInitialSize((500, 300))

def create(canvas, window):
  return MenuBar(canvas, window)
