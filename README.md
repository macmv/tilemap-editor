
Structure:
* Tilemap
  * contains a Toolbar instance, to know what to do on mouse clicks
  * handles mouse clicks in that area
  * can save/load from disk
* Canvas
  * is the thing in the middle that you draw on
  * draws the cursor and all the tiles
  * not actaully seperate from the Tilemap in the code
* Toolbar
  * is the column on the left that has all the tools
  * contains Tileset instance, to know which tile to paint on with the tile paint tool
  * contains ToolSettings instance, to know what crap is happening with the brush
* Tool Settings
  * thing in bottom left
  * color picker and stuff
  * things like scale/opacity
* Tileset
  * is the thing in the top right which shows the tiles u have
  * can select a tile and paint on those tiles with a tool
  * can create/remove tiles
* Pallet
  * it stores the colors you've used recently
  * is a grid of small squares, similar to tileset
  * can set to different presets with a dropdown
* Thing in bottom
  * like in pyxel edit, this will be for animations far in the future
  * doesn't exist
  * don't really care about it


```
                   Tilemap
                      |
               |-------------|
               |             |
            Toolbar        Canvas
               |
        |-------------|-------------|
        |             |             |
  ToolSettings     Tileset        Pallet
```
