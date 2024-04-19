from graphics_pg_plus import *

init()

window = Window(1000, 500, "Test")
input = InputListener()

field = InputField(vec2(500, 250), 250, 125, False)
window.addInputField(field)

def gameLoop():
    field.draw(window, 20, "Arial", rgb(0, 0, 0), rgb(0, 0, 0), True, 6, rgb(255, 255, 255), rgb(160, 0, 0))
    return

window.startGameLoop(gameLoop, "ESCAPE", 60, input)

quit()