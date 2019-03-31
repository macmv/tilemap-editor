
from PIL import Image
import math
import tilemap_pb2

class FileManager:
  def __init__(self, canvas):
    self.canvas = canvas

  def save(self, filename):
    print("Saving")
    tileset = self.create_tileset()
    tileset.save(filename + ".png", "PNG")
    proto = self.create_tilemap()
    with open(filename + ".map", "wb") as f:
      f.write(proto.SerializeToString())

  def create_tileset(self):
    tileset = self.canvas.tileset
    tiles = tileset.tiles
    length = len(tiles)
    tileset_width = 5 # 5 tiles per line. Change in settings in future
    tile_width = tileset.get_tile_width()
    tile_height = tileset.get_tile_height()
    tileset_image = Image.new('RGB',
        (tile_width * tileset_width,
        tile_height * (int(length / tileset_width) + 1)),
        'black')
    tileset_image.putalpha(0)
    index = 0
    for tile in tileset.tiles:
      pil_img = tile.img
      tileset_image.paste(pil_img,
        ((index % tileset_width) * tile_width,
        int(index / tileset_width) * tile_height),
        pil_img)
      index += 1
    return tileset_image

  def create_tilemap(self):
    tilemap = self.canvas.tilemap
    proto = tilemap_pb2.Tilemap()
    for x, y in tilemap:
      proto.tiles[y * self.canvas.width + x] = tilemap[(x, y)]
    proto.tileWidth = self.canvas.tileset.get_tile_width()
    proto.tileHeight = self.canvas.tileset.get_tile_height()
    proto.width = self.canvas.width
    proto.height = self.canvas.height
    return proto

  def load(self, filename):
    # do crap
    pass

  def load_tileset(self, filename):
    # load the image and do crap
    pass
