
from PIL import Image
import math
import tilemap_pb2
import io

class FileManager:
  def __init__(self, canvas):
    self.canvas = canvas

  def save(self, filename):
    print("Saving")
    proto = self.create_tilemap()
    tileset = self.create_tileset(proto)
    with open(filename + ".map", "wb") as f:
      f.write(proto.SerializeToString())

  def get_tileset_length(self):
    tileset = self.canvas.tileset
    tiles = tileset.tiles
    return len(tiles)

  def create_tileset(self, proto):
    tileset = self.canvas.tileset
    tiles = tileset.tiles
    length = len(tiles)
    tileset_width = 5 # 5 tiles per line. Change in settings in future
    tile_width = tileset.get_tile_width()
    tile_height = tileset.get_tile_height()
    for tile in tileset.tiles:
      tile_proto = proto.tileset.add()
      tile_proto.width = tile_width
      tile_proto.height = tile_height
      img_byte_arr = io.BytesIO()
      tile.img.save(img_byte_arr, format='PNG')
      img_byte_arr = img_byte_arr.getvalue()
      tile_proto.image_data = img_byte_arr

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
    tileset_arr = self.load_tileset(proto)
    return tileset_arr, proto

  def load_tileset(self, proto): # creates an array of images
    tileset_bytes = proto.tileset
    tileset_arr = []
    for tile_data in tileset_bytes:
      tileset_arr.append(Image.open(io.BytesIO(tile_data.image_data)))
    return tileset_arr
