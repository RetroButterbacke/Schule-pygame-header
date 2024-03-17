import graphics as g
from typing import List
import random

g.init()
window = g.createWindow(1000, 500, "Snake", 0)
g.setClearColor(g.rgb(7, 207, 177))

SnakeHead: g.vec2
SnakeBody: List[g.vec2] = []
Apple: g.vec2

startGame: bool = False
isGameOver: bool = False
tunneling: bool = False

drawGrid: bool = False
tileSize: int = 20

valocity_x: int = 0
valocity_y: int = 0

lastKeys: List[str] = ["None"]

HighScore: int = 0

def applePos() -> g.vec2:
    pos = g.vec2((random.randint(0, (window.get_width() - 1)//tileSize) * tileSize) + tileSize // 2, (random.randint(0, (window.get_height() - 1)//tileSize) * tileSize) + tileSize // 2)
    for _ in range(0, (window.get_width() - 1) // tileSize * (window.get_height() - 1) // tileSize):
        inBody: bool = False
        for tile in SnakeBody:
            if tile == pos:
                inBody = True
        if pos != SnakeHead and not inBody:
            return pos
        else:
            pos.x += 1
            if (pos.x > (window.get_width() - 1) // tileSize):
                pos.x = tileSize//2
                pos.y += 1

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
            HighScore = len(SnakeBody)
            startGame = False
            isGameOver = True
            return
    else:
        if SnakeHead.x > window.get_width():
            SnakeHead.x = tileSize//2
            return
        elif SnakeHead.x < 0:
            SnakeHead.x = window.get_width() - tileSize//2
            return
        elif SnakeHead.y > window.get_height():
            SnakeHead.y = tileSize // 2
            return
        elif SnakeHead.y < 0:
            SnakeHead.y = window.get_height() - tileSize//2
            return

    for tile in SnakeBody:
        if SnakeHead == tile:
            HighScore = len(SnakeBody)
            startGame = False
            isGameOver = True
            return
                
    if SnakeHead == Apple:
        SnakeBody.append(Apple)
        Apple = applePos()

    if len(SnakeBody) != 0:
        for i in range(len(SnakeBody), 0, -1):
            if i - 1 > 0:
                SnakeBody[i-1] = g.vec2(SnakeBody[i - 2].x, SnakeBody[i - 2].y)
            else:
                SnakeBody[0] = g.vec2(SnakeHead.x, SnakeHead.y)

    SnakeHead.x += tileSize * valocity_x
    SnakeHead.y += tileSize * valocity_y
    return    

# It is recommended to not create to many timers it can cause lag the best is you create only one and one function that handels the timed updates
timer: g.Timer = g.Timer(200, calculateNext)

def start():
    global SnakeHead
    global Apple
    global startGame
    global valocity_x
    global valocity_y

    print(startGame)

    if not startGame:
        if random.randint(1, 2) == 1:
            valocity_x = random.choice([-1, 1])
        else:
            valocity_x = random.choice([-1, 1])
        SnakeHead = g.vec2((random.randint(0, (window.get_width() - 1)//tileSize) * tileSize) + tileSize // 2, (random.randint(0, (window.get_height() - 1)//tileSize) * tileSize) + tileSize // 2)
        Apple = applePos()
        startGame = True
        timer.start()
    return
    

def reset():
    SnakeBody.clear()
    start()
    return

def setTunneling():
    global tunneling
    tunneling = not tunneling

startButton = g.Button(100, 50, g.vec2(500, 300), "Start", start)
retryButton = g.Button(100, 50, g.vec2(500, 300), "Retry", reset)
quitButton = g.Button(100, 50, g.vec2(500, 360), "Quit", lambda: g.quit())
tunnelingButton = g.Button(tileSize, tileSize, g.vec2((tileSize * 4) + tileSize // 2, tileSize // 2), None, lambda: setTunneling())
g.addButton(retryButton)
g.addButton(startButton)
g.addButton(quitButton)
g.addButton(tunnelingButton)

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

    if g.wasKeyPressed("Z"):
        drawGrid = not drawGrid
    if g.wasKeyPressed("W") and valocity_y != 1 and lastKeys[-1] != "S":
        lastKeys.append("W")
    if g.wasKeyPressed("A") and valocity_x != 1 and lastKeys[-1] != "D":
        lastKeys.append("A")
    if g.wasKeyPressed("S") and valocity_y != -1 and lastKeys[-1] != "W":
        lastKeys.append("S")
    if g.wasKeyPressed("D") and valocity_x != -1 and lastKeys[-1] != "A":
        lastKeys.append("D")

    if g.wasKeyPressed("R"):
        if startGame:
            HighScore = len(SnakeBody)
            startGame = False
            isGameOver = True
            timer.stop()

    if drawGrid:
        for y in range(1, window.get_height() - 1//tileSize):
            g.drawLine(window, g.vec2(0, y * tileSize), g.vec2(1000, y * tileSize), g.rgb(0, 60, 0))
        for x in range(1, window.get_width()//tileSize + 1):
            g.drawLine(window, g.vec2(x * tileSize, 0), g.vec2(x * tileSize, 499), g.rgb(0, 60, 0))

    if startGame:
        g.drawRect(window, Apple, tileSize, tileSize, g.rgb(150, 0, 0))
        g.drawRect(window, Apple, tileSize, tileSize, g.rgb(120, 0, 0), lineDepth=3)
        for tile in SnakeBody:
            g.drawRect(window, tile, tileSize, tileSize, g.rgb(0, 160, 0))
            g.drawRect(window, tile, tileSize, tileSize, g.rgb(0, 120, 0), lineDepth=3)
        g.drawRect(window, SnakeHead, tileSize, tileSize, g.rgb(0, 120, 0))
        g.drawRect(window, SnakeHead, tileSize, tileSize, g.rgb(0, 160, 0), lineDepth=3)
        g.drawText(window, g.vec2(window.get_width() - 50, 13), 80, 50, f"Score: {len(SnakeBody)}")
        g.drawText(window, g.vec2(window.get_width() - 70, 45), 120, 50, f"HighScore: {HighScore}")
    elif isGameOver:
        timer.stop()
        g.drawRect(window, Apple, tileSize, tileSize, g.rgb(150, 0, 0))
        g.drawRect(window, Apple, tileSize, tileSize, g.rgb(120, 0, 0), lineDepth=3)
        for tile in SnakeBody:
            g.drawRect(window, tile, tileSize, tileSize, g.rgb(0, 160, 0))
            g.drawRect(window, tile, tileSize, tileSize, g.rgb(0, 120, 0), lineDepth=3)
        g.drawRect(window, SnakeHead, tileSize, tileSize, g.rgb(0, 120, 0))
        g.drawRect(window, SnakeHead, tileSize, tileSize, g.rgb(0, 160, 0), lineDepth=3)
        g.drawText(window, g.vec2(window.get_width() // 2, (window.get_height() // 2) - 100), 400, 250, "Game Over", g.rgb(150, 0, 0))
        g.drawText(window, g.vec2(window.get_width() // 2, (window.get_height() // 2) - 30), 300, 150, f"HighScore: {HighScore}")
        retryButton.draw(window, 0, "Arial", g.rgb(0, 0, 60), True, 3, g.rgb(250, 232, 14), g.rgb(147, 24, 0))
        quitButton.draw(window, 0, "Arial", g.rgb(0, 0, 60), True, 3, g.rgb(250, 232, 14), g.rgb(147, 24, 0))
    else:
        g.drawText(window, g.vec2(window.get_width() // 2, (window.get_height() // 2) - 100), 400, 250, "Snake", g.rgb(0, 160, 0))
        startButton.draw(window, 0, "Arial", g.rgb(0, 0, 60), True, 3, g.rgb(250, 232, 14), g.rgb(147, 24, 0))
        quitButton.draw(window, 0, "Arial", g.rgb(0, 0, 60), True, 3, g.rgb(250, 232, 14), g.rgb(147, 24, 0))
        g.drawText(window, g.vec2(window.get_width() - 80, 13), 120, 50, f"HighScore: {HighScore}")

    g.drawText(window, g.vec2(tileSize * 2, tileSize // 2), tileSize * 4, tileSize * 2, "Tunneling")
    tunnelingButton.draw(window, 0, "Arial", g.rgb(0, 0, 0), True, int(tileSize * 0.2), g.rgb(255, 255, 255), g.rgb(0, 50, 0))
    if tunneling:
        g.drawRect(window, g.vec2((tileSize * 4) + tileSize // 2, tileSize // 2), tileSize, tileSize, g.rgb(0, 50, 0))
    return

g.startGameLoop(gameLoop, window, "ESCAPE", 60)