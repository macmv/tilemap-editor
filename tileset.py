import wx
import array
import cairo
from PIL import Image
import image_button

# Stores all the tiles created. Can be selected and drawn onto canvas to be edited
class Tileset():
  def __init__(self, pnl, tile_width, tile_height):
    self.tile_width = tile_width
    self.tile_height = tile_height
    self.tiles = [] # array of Tile objects
    self.selected_tile_id = -1 # index of tile selected in gui

    sizer = wx.BoxSizer(wx.VERTICAL)
    self.box = wx.Panel(pnl) # main container for everything
    self.box.SetSizer(sizer)

    self.buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.buttons_box = wx.Panel(self.box) # container for add / delete buttons
    sizer.Add(self.buttons_box, 0, wx.ALL, 5)
    self.buttons_box.SetSizer(self.buttons_sizer)

    self.new_button = wx.BitmapButton(self.buttons_box, bitmap=wx.Bitmap("assets/pencil.png"))
    self.buttons_sizer.Add(self.new_button, 0, wx.ALL, 5)
    self.new_button.Bind(wx.EVT_BUTTON, self.add)

    self.delete_button = wx.BitmapButton(self.buttons_box, bitmap=wx.Bitmap("assets/eraser.png"))
    self.buttons_sizer.Add(self.delete_button, 0, wx.ALL, 5)
    self.delete_button.Bind(wx.EVT_BUTTON, self.remove_selected)

    self.da = wx.Panel(self.box) # will draw tiles in here
    sizer.Add(self.da, 1, wx.EXPAND, 5)
    self.da.Bind(wx.EVT_PAINT, self.draw)
    self.da.Bind(wx.EVT_LEFT_DOWN, self.click)

    self.pixel_size = 4 # this should be the width of the tileset / tiles_per_row / tile_width
    self.tiles_per_row = 2 # this should be defined based on how big we want the tiles to be

    self.add(None)

  def widget(self):
    return self.box

  def update(self):
    self.da.Refresh()

  def load_tileset(self, width, height, tileset):
    self.tile_width = width
    self.tile_height = height
    self.tiles = []
    for image in tileset:
      self.add(None)
      tile = self.tiles[len(self.tiles) - 1]
      tile.load_image(image)

  def get_tile_width(self):
    return self.tile_width

  def get_tile_height(self):
    return self.tile_height

  def add(self, event):
    self.tiles.append(Tile(self.tile_width, self.tile_height, len(self.tiles)))
    self.da.Refresh()

  def get(self, tile_id):
    return self.tiles[tile_id]

  def remove_selected(self, event):
    if self.selected_tile_id == -1:
      return
    tile = self.tiles[self.selected_tile_id]
    del self.tiles[self.selected_tile_id]
    if self.selected_tile_id >= len(self.tiles):
      self.selected_tile_id = -1
    self.da.Refresh()

  def click(self, event):
    tile_x = int(event.GetX() / self.tile_width / self.pixel_size)
    tile_y = int(event.GetY() / self.tile_height / self.pixel_size)
    index = tile_y * self.tiles_per_row + tile_x
    self.select(index)

  def select(self, index):
    if index >= len(self.tiles):
      index = -1
    self.selected_tile_id = index
    self.da.Refresh()

  def draw(self, event):
    dc = wx.PaintDC(self.da)
    ctx = wx.lib.wxcairo.ContextFromDC(dc)
    i = 0
    for tile in self.tiles:
      tile.draw(ctx, self.pixel_size, (i % self.tiles_per_row * 9 / 8, int(i / self.tiles_per_row) * 9 / 8))
      i += 1
    if self.selected_tile_id >= 0:
      x = self.selected_tile_id % self.tiles_per_row * self.tile_width * self.pixel_size
      y = int(self.selected_tile_id / self.tiles_per_row) * self.tile_height * self.pixel_size
      ctx.set_source_rgb(1, 1, 1)
      ctx.rectangle(x * 9 / 8, y * 9 / 8, self.tile_width * self.pixel_size, self.tile_height * self.pixel_size)
      ctx.stroke()

  def get_selected_tile(self):
    return self.selected_tile_id

  def destroy(self):
    raise "no yeetage"
    for tile in self.tiles:
      tile.destroy()
    self.da.destroy()

# Single tile. Will be drawn multiple times on canvas
class Tile():
  def __init__(self, width, height, index):
    self.width = width
    self.height = height
    self.img = Image.new('RGB', (width, height), 'black')
    self.img.putalpha(256)
    self.pixels = self.img.load()
    self.update_pattern()

  def draw_button(self, widget, ctx):
    mat = cairo.Matrix() # to get rid of the translation on the pattern when drawing on the canvas
    self.pattern.set_matrix(mat)
    ctx.scale(widget.get_allocated_width() / self.img.width,
        widget.get_allocated_height() / self.img.height)
    ctx.set_source(self.pattern)
    ctx.paint()

  def widget(self):
    return self.button

  def load_image(self, img):
    if img.width != self.width or img.height != self.height:
      raise "WTF NOT GOOD IMG"
    self.img = img
    self.pixels = self.img.load()
    self.update_pattern()

  def update_pattern(self):
    arr = bytearray(self.img.tobytes('raw', 'BGRa'))
    surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, self.img.width, self.img.height)
    self.pattern = cairo.SurfacePattern(surface)
    self.pattern.set_filter(cairo.FILTER_NEAREST)

  def get_width(self):
    return self.width

  def get_height(self):
    return self.height

  def get_pixel(self, x, y):
    r, g, b, a = self.pixels[x, y]
    return (r, g, b)

  def set_pixel(self, x, y, color):
    self.pixels[x, y] = tuple([int(i) for i in color])
    self.update_pattern()

  def draw(self, ctx, pixel_size, tile_pos):
    tile_x, tile_y = tile_pos
    mat = cairo.Matrix() # apparently this needs to be negative ¯\_(ツ)_/¯
    mat.translate(-tile_x * self.width, -tile_y * self.height)
    mat.scale(1 / pixel_size, 1 / pixel_size)
    self.pattern.set_matrix(mat)
    ctx.set_source(self.pattern)
    ctx.rectangle(tile_x * self.width * pixel_size,
            tile_y * self.height * pixel_size,
            self.width * pixel_size,
            self.height * pixel_size)
    ctx.fill()

  def __repr__(self):
    return "Tile <index=" + str(self.button.index) + ">"

def create(pnl, width, height):
  return Tileset(pnl, width, height)
