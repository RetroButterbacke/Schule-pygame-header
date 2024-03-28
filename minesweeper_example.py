from graphics_h import * 
from typing import Dict, List
import random

init()

window = Window(1000, 500, "Minesweeper")
window.setClearColor(rgb(210, 210, 210))

input = InputListener()

tileSize: int = 20

grid_start_x: int = 0
grid_start_y: int = 0
move_x = 30
move_y = 40
x_end: int = (window.get_width() - (grid_start_x + move_x * 2)) // tileSize
y_end: int = (window.get_height() - (grid_start_y + move_y)) // tileSize
redraw: bool = True

grid: Surface = Surface(*window.get_size())

for x in range(grid_start_x, x_end):
    for y in range(grid_start_y, y_end):
        grid.drawLine(vec2((x * tileSize) + (move_x + 2), (move_y - 2)), vec2((x * tileSize) + (move_x + 2), (move_y - 2) + (y_end * tileSize)), rgb(162, 162, 162), 2)
        grid.drawLine(vec2(move_x + 2, (y * tileSize) + (move_y - 2)), vec2((move_x + 2) + (x_end * tileSize), (move_y - 2) + (y * tileSize)), rgb(162, 162, 162), 2)
grid.drawLine(vec2((move_x + 2) + (x_end * tileSize), (move_y - 2)), vec2((move_x + 2) + (x_end * tileSize), (move_y - 2) + (y_end * tileSize)), rgb(162, 162, 162), 2)
grid.drawLine(vec2((move_x + 4), (move_y - 2) + (y_end * tileSize)), vec2((move_x + 2) + (x_end * tileSize), (move_y - 2) + (y_end * tileSize)), rgb(162, 162, 162), 2) 

print(f"Currently rendering {x_end * y_end} tiles")

bombNumber: int = 10

tiles: Dict[vec2, bool] = {}
saroundingBombs: Dict[vec2, int] = {}
bombs: List[vec2] = []


for x in range(x_end):
    for y in range(y_end):
        tile_pos = vec2(x, y)
        if tile_pos not in tiles:
            tiles[tile_pos] = True	

for _ in range(bombNumber):
    bombs.append(vec2(random.randint(0, x_end - 1), random.randint(0, y_end - 1)))

for tile, value in tiles.items():
    saroundingPoses: List[vec2] = []
    saroundingPoses.append(vec2(tile.x - 1, tile.y - 1))
    saroundingPoses.append(vec2(tile.x, tile.y - 1))
    saroundingPoses.append(vec2(tile.x + 1, tile.y - 1))
    saroundingPoses.append(vec2(tile.x + 1, tile.y))
    saroundingPoses.append(vec2(tile.x + 1, tile.y + 1))
    saroundingPoses.append(vec2(tile.x, tile.y + 1))
    saroundingPoses.append(vec2(tile.x - 1, tile.y + 1))
    saroundingPoses.append(vec2(tile.x - 1, tile.y))
    numSaroundingBombs: int = 0
    for bomb in bombs:
        if bomb in saroundingPoses:
            numSaroundingBombs += 1
    saroundingBombs[tile] = numSaroundingBombs

def open(tile: vec2) -> None:
    
    return    

def gameLoop():
    global redraw
    global tiles

    if window.getTimeDiff() >= 1:
        print(window.getFPS())

    if (((x_end + 1) * (y_end + 1))//tileSize)-2 > 1000:
        print(f"Too many tiles = lag. The game tried to render: {x_end * y_end} tiles.") 
        window.quit()
        return 

    if input.wasKeyPressed("K"):
        print(tiles)

    if input.wasButtonPressed("LEFT"):
        mousePos = window.getMousePos()
        if move_x <= mousePos.x < (x_end * tileSize) + move_x and move_y <= mousePos.y < (y_end * tileSize) + move_y:
            pos = vec2(((mousePos.x - move_x) // tileSize), ((mousePos.y - move_y) // tileSize))
            tiles[pos] = False
        redraw = True

    if redraw:
        window.clear()

        window.drawSurface(vec2(0, 0), grid)

        for tile, value in tiles.items():
            if value:
                window.drawRect(vec2(((tile.x * tileSize) + (tileSize // 2)) + (move_x + 2), ((tile.y * tileSize) + (tileSize // 2)) + (move_y - 2)), tileSize, tileSize, rgb(219, 219, 219))
                window.drawRect(vec2(((tile.x * tileSize) + (tileSize // 2)) + (move_x + 2), ((tile.y * tileSize) + (tileSize // 2)) + (move_y - 2)), tileSize, tileSize, rgb(162, 162, 162), lineDepth=1)
            else:
                if saroundingBombs[tile] > 0:
                    window.drawText(vec2(((tile.x * tileSize) + (tileSize // 2)) + (move_x + 2), ((tile.y * tileSize) + (tileSize // 2)) + (move_y - 2)), tileSize, tileSize, f"{saroundingBombs[tile]}")
                else:
                    open(tile)

        for tile in bombs:
            window.drawRect(vec2(((tile.x * tileSize) + (tileSize // 2)) + (move_x + 2), ((tile.y * tileSize) + (tileSize // 2)) + (move_y - 2)), tileSize, tileSize, rgb(150, 0, 0))

        redraw = False

    return

window.startGameLoop(gameLoop, "ESCAPE", 60, input)

quit()
