
Structure:
  Tilemap
    contains a Toolbar instance, to know what to do on mouse clicks
    is the thing in the middle that you draw on
    handles mouse clicks in that area
  Toolbar
    is the column on the left that has all the tools
    contains Tileset instance, to know which tile to paint on with the tile paint tool
    contains BrushOptions instance, to know what crap is happening with the brush
  BrushOptions
    thing in bottom left
    like color picker and stuff
    things like scale/opacity
  Tileset
    is the thing in the top right which shows the tiles u have
    can select a tile and paint on those tiles with a tool
    can create/remove tiles
  Thing in the bottom right
    y is it there
    maybe like color pallet
    maybe layers
  Thing in bottom
    like in pyxel edit, this will be 4 animations far in the future
    doesn't exist
    don't really care about it
