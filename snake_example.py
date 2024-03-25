from graphics_h import *
from typing import List
import random
import pygame as pg

init()

# windowflags = pg.FULLSCREEN | pg.OPENGL
# window = Window(1920, 1080, "Snake", window_flags=windowflags)
window = Window(1000, 500, "Snake")
window.setClearColor(rgb(7, 207, 177))

SnakeHead: vec2
SnakeBody: List[vec2] = []
Apple: vec2

startGame: bool = False
isGameOver: bool = False
tunneling: bool = False

drawGrid: bool = False
tileSize: int = 20

valocity_x: int = 0
valocity_y: int = 0

lastKeys: List[str] = ["None"]

grid: Surface = Surface(*window.getSize())

HighScore: int = 0

def applePos() -> vec2:
    pos = vec2((random.randint(0, (window.get_width() - 1)//tileSize) * tileSize) + tileSize // 2, (random.randint(0, (window.get_height() - 1)//tileSize) * tileSize) + tileSize // 2)
    for _ in range((window.get_width() - 1) // tileSize * (window.get_height() - 1) // tileSize):
        inBody: bool = False
        for tile in SnakeBody:
            if tile == pos:
                inBody = True
        if pos != SnakeHead and not inBody:
            return pos
        else:
            pos += vec2(tileSize, 0)
            if (pos.x > (window.get_width() - 1) // tileSize):
                pos += vec2(tileSize, tileSize)

def calculateNext():
    global Apple
    global SnakeHead
    global SnakeBody
    global valocity_x
    global valocity_y
    global HighScore
    global startGame
    global isGameOver
    global lastKeys

    lastKey: str = "None"

    if len(lastKeys) > 1:
        lastKey = lastKeys[1]

    if lastKey == "W":
        valocity_x = 0
        valocity_y = -1
        lastKeys.pop(1)
    elif lastKey == "A":
        valocity_x = -1
        valocity_y = 0
        lastKeys.pop(1)
    elif lastKey == "S":
        valocity_x = 0
        valocity_y = 1
        lastKeys.pop(1)
    elif lastKey == "D":
        valocity_x = 1
        valocity_y = 0
        lastKeys.pop(1)

    if not tunneling:
        if SnakeHead.x + tileSize * valocity_x > window.get_width() - 1 or SnakeHead.y + tileSize * valocity_y > window.get_height() - 1 or SnakeHead.x + tileSize * valocity_x < 0 or SnakeHead.y + tileSize * valocity_y < 0:
            HighScore = len(SnakeBody) if len(SnakeBody) > HighScore else HighScore
            startGame = False
            isGameOver = True
            return
    else:
        if SnakeHead.x > window.get_width():
            SnakeHead = vec2(tileSize//2, SnakeHead.y)
            return
        elif SnakeHead.x < 0:
            SnakeHead = vec2(window.get_width() - tileSize//2, SnakeHead.y)
            return
        elif SnakeHead.y > window.get_height():
            SnakeHead = vec2(SnakeHead.x, tileSize // 2)
            return
        elif SnakeHead.y < 0:
            SnakeHead = vec2(SnakeHead.x, window.get_height() - tileSize//2)
            return

    for tile in SnakeBody:
        if SnakeHead == tile:
            HighScore = len(SnakeBody) if len(SnakeBody) > HighScore else HighScore            
            startGame = False
            isGameOver = True
            return
                
    if SnakeHead == Apple:
        SnakeBody.append(Apple)
        Apple = applePos()

    if len(SnakeBody) != 0:
        for i in range(len(SnakeBody), 0, -1):
            if i - 1 > 0:
                SnakeBody[i-1] = vec2(SnakeBody[i - 2].x, SnakeBody[i - 2].y)
            else:
                SnakeBody[0] = vec2(SnakeHead.x, SnakeHead.y)

    SnakeHead += vec2(tileSize * valocity_x, tileSize * valocity_y)
    return    

# It is recommended to not create to many timers it can cause lag the best is you create only one and one function that handels the timed updates
timer: Timer = Timer(200, calculateNext)

def start():
    global SnakeHead
    global Apple
    global startGame
    global valocity_x
    global valocity_y

    if not startGame:
        if random.randint(1, 2) == 1:
            valocity_x = random.choice([-1, 1])
        else:
            valocity_y = random.choice([-1, 1])
        SnakeHead = vec2((random.randint(0, (window.get_width() - 1)//tileSize) * tileSize) + tileSize // 2, (random.randint(0, (window.get_height() - 1)//tileSize) * tileSize) + tileSize // 2)
        Apple = applePos()
        startGame = True
        timer.start()
    return
    

def reset():
    global valocity_x
    global valocity_y
    valocity_x = 0
    valocity_y = 0
    SnakeBody.clear()
    start()
    return

def setTunneling():
    global tunneling
    tunneling = not tunneling

startButton = Button(100, 50, vec2(500, 300), "Start", start)
retryButton = Button(100, 50, vec2(500, 300), "Retry", reset)
quitButton = Button(100, 50, vec2(500, 360), "Quit", lambda: window.quit())
tunnelingButton = Button(tileSize, tileSize, vec2((tileSize * 4) + tileSize // 2, tileSize // 2), None, setTunneling)
window.addButton(retryButton)
window.addButton(startButton)
window.addButton(quitButton)
window.addButton(tunnelingButton)

def gameLoop():
    global drawGrid
    global tileSize
    global SnakeHead
    global SnakeBody
    global Apple
    global valocity_x
    global valocity_y
    global lastKeys
    global startGame
    global isGameOver
    global HighScore
    global grid

    window.clear()

    if window.getTimeDiff() >= 1:
        print(window.getFPS())

    if window.wasKeyPressed("Z"):
        drawGrid = not drawGrid
        if not drawGrid:
            for x in range(1, window.get_width() // tileSize):
                for y in range(1, window.get_height() // tileSize):
                    grid.drawLine(vec2(x * tileSize, 0), vec2(x * tileSize, window.get_height() - 1), rgb(0, 60, 0))
                    grid.drawLine(vec2(0, y * tileSize), vec2(window.get_width() - 1, y * tileSize), rgb(0, 60, 0))
        else:
            grid.clear()
        
    if window.wasKeyPressed("W") and valocity_y != 1:
        lastKeys.append("W")
    if window.wasKeyPressed("A") and valocity_x != 1:
        lastKeys.append("A")
    if window.wasKeyPressed("S") and valocity_y != -1:
        lastKeys.append("S")
    if window.wasKeyPressed("D") and valocity_x != -1:
        lastKeys.append("D")

    if window.wasKeyPressed("R"):
        if startGame:
            HighScore = len(SnakeBody) if len(SnakeBody) > HighScore else HighScore
            startGame = False
            isGameOver = True
            timer.stop()

    window.drawSurface(vec2(0, 0), grid)

    if startGame:
        window.drawRect(Apple, tileSize, tileSize, rgb(150, 0, 0))
        window.drawRect(Apple, tileSize, tileSize, rgb(120, 0, 0), lineDepth=3)
        for tile in SnakeBody:
            window.drawRect(tile, tileSize, tileSize, rgb(0, 160, 0))
            window.drawRect(tile, tileSize, tileSize, rgb(0, 120, 0), lineDepth=3)
        window.drawRect(SnakeHead, tileSize, tileSize, rgb(0, 120, 0))
        window.drawRect(SnakeHead, tileSize, tileSize, rgb(0, 160, 0), lineDepth=3)
        window.drawText(vec2(window.get_width() - 50, 13), 80, tileSize, f"Score: {len(SnakeBody)}")
        window.drawText(vec2(window.get_width() - 67, 35), 120, tileSize, f"HighScore: {HighScore}")
    elif isGameOver:
        timer.stop()
        window.drawRect(Apple, tileSize, tileSize, rgb(150, 0, 0))
        window.drawRect(Apple, tileSize, tileSize, rgb(120, 0, 0), lineDepth=3)
        for tile in SnakeBody:
            window.drawRect(tile, tileSize, tileSize, rgb(0, 160, 0))
            window.drawRect(tile, tileSize, tileSize, rgb(0, 120, 0), lineDepth=3)
        window.drawRect(SnakeHead, tileSize, tileSize, rgb(0, 120, 0))
        window.drawRect(SnakeHead, tileSize, tileSize, rgb(0, 160, 0), lineDepth=3)
        window.drawText(vec2(window.get_width() // 2, (window.get_height() // 2) - 120), 400, tileSize*4, "Game Over", rgb(150, 0, 0))
        window.drawText(vec2(window.get_width() // 2, (window.get_height() // 2) - 65), 240, tileSize*3, f"Score: {len(SnakeBody)}")
        window.drawText(vec2(window.get_width() // 2, (window.get_height() // 2) - 25), 240, tileSize*2, f"HighScore: {HighScore}")
        retryButton.draw(window, 0, "Arial", rgb(0, 0, 60), True, 3, rgb(250, 232, 14), rgb(147, 24, 0))
        quitButton.draw(window, 0, "Arial", rgb(0, 0, 60), True, 3, rgb(250, 232, 14), rgb(147, 24, 0))
        window.drawText(vec2(tileSize * 2, tileSize // 2), tileSize * 4, tileSize, "Tunneling")
        tunnelingButton.draw(window, 0, "Arial", rgb(0, 0, 0), True, int(tileSize * 0.2), rgb(255, 255, 255), rgb(0, 0 ,0))
        if tunneling:
            window.drawRect(vec2((tileSize * 4) + tileSize // 2, tileSize // 2), tileSize, tileSize, rgb(0, 0, 0))
    else:
        window.drawText(vec2(window.get_width() // 2, (window.get_height() // 2) - 100), 400, 250, "Snake", rgb(0, 160, 0))
        startButton.draw(window, 0, "Arial", rgb(0, 0, 60), True, 3, rgb(250, 232, 14), rgb(147, 24, 0))
        quitButton.draw(window, 0, "Arial", rgb(0, 0, 60), True, 3, rgb(250, 232, 14), rgb(147, 24, 0))
        window.drawText(vec2(window.get_width() - 70, 13), 120, tileSize, f"HighScore: {HighScore}")
        window.drawText(vec2(tileSize * 2, tileSize // 2), tileSize * 4, tileSize, "Tunneling")
        tunnelingButton.draw(window, 0, "Arial", rgb(0, 0, 0), True, int(tileSize * 0.2), rgb(255, 255, 255), rgb(0, 0 ,0))
        if tunneling:
            window.drawRect(vec2((tileSize * 4) + tileSize // 2, tileSize // 2), tileSize, tileSize, rgb(0, 0, 0))
    return

window.startGameLoop(gameLoop, "ESCAPE", 60)

quit()