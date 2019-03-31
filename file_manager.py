
from PIL import Image

class FileManager:
  def __init__(self, canvas):
    self.canvas = canvas

  def save(self, filename):
    pil_img = create_tileset()
    # save to 'filename'.png
    protobuf = create_tilemap()
    # save to 'filename'.map

  def create_tileset(self):
    tileset = self.canvas.tileset
    tiles = tileset.tiles
    length = len(tiles)
    tileset_width = 5 # 5 tiles per line. Change in settings in future
    tile_width = tileset.get_tile_width()
    tile_height = tileset.get_tile_height()
    tileset_image = Image.new('RGB', (tile_width * tileset_width, tile_height * (length / tileset_width)), 'black')
    tileset_image.putalpha(256)
    for tile in tileset.tiles:
      pil_img = tile.img
      # add pil_img at correct x and y to tileset_image
    return tileset_image

  def save_tilemap(self):
    # get all the tile ids in the canvas and store it in a Tilemap protobuf
    pass

  def load(self, filename):
    # do crap
    pass

  def load_tileset(self, filename)
    # load the image and do crap
    pass
