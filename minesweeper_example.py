import graphics as g
from typing import Dict, List
import random
import pygame

g.init()
window = g.createWindow(1000, 500, "Minesweeper")
g.setClearColor(g.rgb(210, 210, 210))

tileSize: int = 20

grid_start_x: int = 0
grid_start_y: int = 0
move_x = 30
move_y = 40
x_end: int = (window.get_width() - (grid_start_x + move_x * 2)) // tileSize
y_end: int = (window.get_height() - (grid_start_y + move_y)) // tileSize

print(f"Currently rendering {x_end * y_end} tiles")

bombNumber: int = 10

tiles: Dict[g.vec2, bool] = {}
saroundingBombs: Dict[g.vec2, int] = {}
bombs: List[g.vec2] = []


for x in range(x_end):
    for y in range(y_end):
        tile_pos = g.vec2(x, y)
        if tile_pos not in tiles:
            tiles[tile_pos] = True

for _ in range(bombNumber):
    bombs.append(g.vec2(random.randint(0, x_end), random.randint(0, y_end)))

for tile, value in tiles.items():
    saroundingPoses: List[g.vec2] = []
    saroundingPoses.append(g.vec2(tile.x - 1, tile.y - 1))
    saroundingPoses.append(g.vec2(tile.x, tile.y - 1))
    saroundingPoses.append(g.vec2(tile.x + 1, tile.y - 1))
    saroundingPoses.append(g.vec2(tile.x + 1, tile.y))
    saroundingPoses.append(g.vec2(tile.x + 1, tile.y + 1))
    saroundingPoses.append(g.vec2(tile.x, tile.y + 1))
    saroundingPoses.append(g.vec2(tile.x - 1, tile.y + 1))
    saroundingPoses.append(g.vec2(tile.x - 1, tile.y))
    numSaroundingBombs: int = 0
    for bomb in bombs:
        for t in saroundingPoses:
            if bomb == t:
                numSaroundingBombs += 1
    saroundingBombs[tile] = numSaroundingBombs

last_time = pygame.time.get_ticks()

def gameLoop():
    global tiles
    global last_time

    print((1 / (pygame.time.get_ticks() - last_time)) * 1000)
    last_time = pygame.time.get_ticks()

    if (((x_end + 1) * (y_end + 1))//tileSize)-2 > 1000:
        print(f"Too many tiles = lag. The game tried to render: {x_end * y_end} tiles.") 
        g.quit()
        return

    for x in range(grid_start_x, x_end):
        for y in range(grid_start_y, y_end):
            g.drawLine(window, g.vec2((x * tileSize) + (move_x + 2), (move_y - 2)), g.vec2((x * tileSize) + (move_x + 2), (move_y - 2) + (y_end * tileSize)), g.rgb(162, 162, 162), 2)
            g.drawLine(window, g.vec2(move_x + 2, (y * tileSize) + (move_y - 2)), g.vec2((move_x + 2) + (x_end * tileSize), (move_y - 2) + (y * tileSize)), g.rgb(162, 162, 162), 2)
    g.drawLine(window, g.vec2((move_x + 2) + (x_end * tileSize), (move_y - 2)), g.vec2((move_x + 2) + (x_end * tileSize), (move_y - 2) + (y_end * tileSize)), g.rgb(162, 162, 162), 2)
    g.drawLine(window, g.vec2((move_x + 4), (move_y - 2) + (y_end * tileSize)), g.vec2((move_x + 2) + (x_end * tileSize), (move_y - 2) + (y_end * tileSize)), g.rgb(162, 162, 162), 2)  

    if g.wasKeyPressed("K"):
        print(tiles)

    if g.wasButtonPressed("LEFT"):
        mousePos = g.getMousePos()
        if move_x <= mousePos.x < (x_end * tileSize) + move_x and move_y <= mousePos.y < (y_end * tileSize) + move_y:
            pos = g.vec2(((mousePos.x - move_x) // tileSize), ((mousePos.y - move_y) // tileSize))
            tiles[pos] = False

    for tile, value in tiles.items():
        if value:
            g.drawRect(window, g.vec2(((tile.x * tileSize) + (tileSize // 2)) + (move_x + 2), ((tile.y * tileSize) + (tileSize // 2)) + (move_y - 2)), tileSize, tileSize, g.rgb(219, 219, 219))
            g.drawRect(window, g.vec2(((tile.x * tileSize) + (tileSize // 2)) + (move_x + 2), ((tile.y * tileSize) + (tileSize // 2)) + (move_y - 2)), tileSize, tileSize, g.rgb(162, 162, 162), lineDepth=1)
        else:
            if saroundingBombs[tile] > 0:
                g.drawText(window, g.vec2(((tile.x * tileSize) + (tileSize // 2)) + (move_x + 2), ((tile.y * tileSize) + (tileSize // 2)) + (move_y - 2)), tileSize, tileSize, f"{saroundingBombs[tile]}")

    for tile in bombs:
        g.drawRect(window, g.vec2(((tile.x * tileSize) + (tileSize // 2)) + (move_x + 2), ((tile.y * tileSize) + (tileSize // 2)) + (move_y - 2)), tileSize, tileSize, g.rgb(150, 0, 0))

    return

g.startGameLoop(gameLoop, window, "ESCAPE", 60)