import graphics_pg_old as g
import os

g.init()
window = g.createWindow(500, 250, "test", 0)
g.setHitboxColor(g.rgb(150,0,0))

############################################
# Initialize Button functions
def test():
    #            Window   pos      width   height  color
    g.drawRect(window, g.vec2(35, 35), 70,      70,     g.rgb(250, 250, 250))
    g.drawRect(window, g.vec2(35, 35), 70,      70,     g.rgb(0, 150, 0), lineDepth=5)
    g.drawCircle(window, g.vec2(400, 170), 70,     g.rgb(150,0,0), g.Texture("./test.jpg"), scaled=False)
    g.drawTriangle(window, g.vec2(200, 170), 70, 70, g.rgb(0, 0, 150), g.Texture("./test.jpg"))
    g.drawText(window, g.vec2(250, 30), 100, 50, "Test", g.rgb(150, 0, 0))
# Initialize Variables
#                      width  height        x    y     label   call on click/ function
test_button = g.Button(70,    30,     g.vec2(250, 125), "test", test)
test2_button = g.Button(70, 30, g.vec2(170, 125), "test", lambda: print("test"))
# Add Buttons
g.addButton(test_button) 
g.addButton(test2_button)
############################################


def gameLoop():
    if g.isKeyPressed("TAB"):
        print(f"{g.getMousePos()[0]}, {g.getMousePos()[1]}")
    if g.isButtonPressed("LEFT"):
        print("LEFT")
    if g.isScrollDir("UP"):
        print("UP")
    if g.isKeyPressed("A"):
        print("Hello, World!")
    if g.isKeyPressed("C"):
        os.system("cls" if os.name == "nt" else "clear")
    if g.isKeyPressed("H"):
        g.showHitboxes(True)
    if g.wasKeyReleased("H"):
        g.showHitboxes(False)
    if g.isKeyPressed("W"):
        g.setClearColor(g.rgb(255, 255, 255))
    if g.wasKeyReleased("W"):
        g.setClearColor(g.rgb(0,0,0))
#                    Window  design fontStyle      fontcolor        outline  outline_depth    bakckground color  outline color
    test_button.draw(window, 0,     "Arial",       g.rgb(0, 0, 0),  True,    2,               g.rgb(250,200,250),     g.rgb(0,0,150)) 
    test2_button.draw(window, 1,     None,         g.rgb(0,0,0),    False,   0,               g.rgb(0, 150, 0), border_radius=20)
    return

g.startGameLoop(gameLoop, window, ("LEFT SHIFT","Q"), 60)
