
from PIL import Image
import math
import tilemap_pb2

class FileManager:
  def __init__(self, canvas):
    self.canvas = canvas

  def save(self, filename):
    print("Saving")
    tileset = self.create_tileset()
    tileset.save(filename, "PNG")
    proto = self.create_tilemap()
    proto.tileset_length = self.get_tileset_length()
    with open(filename[:-4] + ".map", "wb") as f:
      f.write(proto.SerializeToString())

  def get_tileset_length(self):
    tileset = self.canvas.tileset
    tiles = tileset.tiles
    return len(tiles)

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
    proto.tile_width = self.canvas.tileset.get_tile_width()
    proto.tile_height = self.canvas.tileset.get_tile_height()
    proto.width = self.canvas.width
    proto.height = self.canvas.height
    return proto

  def open(self, filename):
    proto = tilemap_pb2.Tilemap()
    with open(filename, "rb") as f:
      proto.ParseFromString(f.read())
      print(proto)
    tileset_arr = self.load_tileset(proto.tile_width,
        proto.tile_height,
        filename)
    return tileset_arr, proto

  def load_tileset(self, tileWidth, tileHeight, filename): # creates an array of images
    tileset_image = Image.open(filename[:-4] + ".png")
    tileset_arr = []
    img_width, img_height = tileset_image.size
    tileset_width = int(img_width / tileWidth)
    tileset_height = int(img_height / tileHeight)
    for y in range(tileset_height):
      for x in range(tileset_width):
        tile_img = tileset_image.crop((x * tileWidth,
            y * tileHeight,
            x * tileWidth + tileWidth,
            y * tileHeight + tileHeight))
        tileset_arr.append(tile_img)
    return tileset_arr
