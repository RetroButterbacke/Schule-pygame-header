import graphics_pg as gh

gh.init()

window = gh.Window(500, 250, "Test")
window.setClearColor(gh.rgb(43, 172, 250))

input = gh.InputListener()

window.clear()
window.drawText(gh.vec2(250, 125), 50, 25, "Test", gh.rgb(150, 0, 0))


def gameLoop():
    if window.getTimeDiff() >= 1:
        print(window.getFPS())

    window.drawRect(gh.vec2(100, 100), 100, 100, gh.rgb(0, 0, 145), "./test.jpg", starting_point=gh.vec2(500, 900), part_width=2000, part_height=500)
    window.drawRect(gh.vec2(100, 210), 100, 100, gh.rgb(0, 0, 145), "./test.jpg", scaled=False, starting_point=gh.vec2(500, 900))
    window.drawTriangle(gh.vec2(400, 100), 50, 50, gh.rgb(0, 10, 0), "./test.jpg")
    window.drawCircle(gh.vec2(250, 200), 30, gh.rgb(0, 10, 0), "./test.jpg")
    return

window.startGameLoop(gameLoop, "ESCAPE", 60, input)

gh.quit()