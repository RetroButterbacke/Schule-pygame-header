!!!old not for the current header!!!


## Needed
#packages
pygame
numpy

#modules
graphics_pg_old(.py)

## Setup

#import
import graphics

#functions
graphics.init()
window = graphics.createWindow(width: int, height: int, caption: str, windowflags: int # wenn man den or(|) operatoren kann man mehrere flags verbinden beispiel: pygame.FULLSCREEN | pygame.OPENGL)

def gameLoop(#muss lehr sein):
  #gameLoop code .....

graphics.startGameLoop(gameLoop, window, caption: str, escapesequence: str oder Tuple[str, ...], framerate: int)

## Functions (for user to use)

init() -> None
isKeyPressed(key: str) -> bool # ist True solange der key gedrückt ist ## "liste" mit möglichen keys sind die values des keys dictionary welches im header ganz oben ist 
wasKeyPressed(key: str) -> bool # ist True in dem moment wo der key gedrückt wurde
wasKeyReleased(key: str) -> bool # ist True in dem moment wo der key losgelassen wurde
isButtonPressed(button: str) -> bool # mit button ist ein mouse button gemeint # LEFT, RIGHT, MIDDLE, WHEEL UP, WHEEL DOWN
wasButtonPressed(button: str) -> bool
wasButtonReleased(button: str) -> bool
isScrollDir(dir: str) -> bool -> bool # Options: UP, DOWN
getMousPos() -> vec2 
getScrollSpeed() -> int
hasMouseMoved() -> bool
setHitboxColor(color: Union[rgb, rgba]) -> None # Hitbox color für die buttons
showHitboxes(show: bool) -> None # Enable/Disable Hitbox drawing

### transparency: range 0 .. 255

drawLine(window, pos1: vec2, pos2: vec2, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), depth: int = 1) -> None
drawRect(window, pos: vec2, width: int, height: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texture: Union[None, Texture] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255, border_radius: int = 0) -> None # der * macht es, dass alles vorm * in der reinfolge ohne variablen namen gegeben werden kann, alles andere muss mit namen beim call benutzt werden
drawCircle(window, pos: vec2, radius: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texture: Union[None, Texture] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None
drawTriangle(window, pos: vec2, width: int, height: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texture: Union[None, Texture] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None
drawTexture(window, pos: vec2, width: int, height: int, texture: Texture, *, rotation: int = 0, transparency: int = 255) -> None
drawText(window, pos: vec2, width: int, height: int, text: str, color: Union[rgb, rgba] = rgba(0, 0, 0, 255), fontStyle: Union[str, None] = None, *, rotation: int = 0, transparency: int = 255) -> None

addButton(button: Button) -> None

createWindow(width: int, height: int, caption: str, window_flags: int) -> pygame.Surface
startGameLoop(gameLoop: Callable, window, escape_sequence: Union[Tuple[str, ...], str], framerate: int) -> None
quit() # quit the game / close window + end program

## classes + uses

# vec2
vec2(x: int, y: int) -> vec2
convert(width: int, height: int, moddifier: str) -> vec2 # modifier's: "ctl", "ctr", "cbl", "cbr", "tl", "tr", "bl", "br"
get() -> Tuple[int, int]

# rgb  # rgba
rgb(red: int, green: int, blue: int) -> rgb
rgba(red: int, green: int, blue: int, alpha: int) -> rgba # alpha in einer range von 0 -> 255
get() -> Tuple[int, int, int(, int)]  
rgb.toRGBA(alpha: int = 255) -> rgba

use: 
  color = rgb(255, 255, 255)
  drawRect(..., color, ...)

# Timer ### stopt wenn program endet
# Am besten startet man nur einen Timer da threads lag erzeugen können wenn zu viele existieren
Timer(delay: int, task: Callable)
start()
stop()

use:
  def calcNext():
    ....
  timer: graphics.Timer = graphics.Timer(100, calcNext)
  timer.start()

# Texture
Texture(filePath: str) -> Texture

´´
get() -> pygame.Surface
getScaled(width: int, height: int) -> pygame.Surface
´´

rotate(rotation: int)

use:
  texture = Texture("./test.jpg")
  drawRect(..., texture, ...)

# Buttons !!!
Button(width: int, height: int, pos: vec2, label: str, runOnClick: Callable) -> Button
                      # 0 or 1: rounded
draw(window, design: int = 0, fontStyle: Union[str, None] = None, fontColor: Union[rgb, rgba] = rgb(0, 0, 0), outlined: bool = False, outline_depth: int = 0, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), outlineColor: Union[rgb, rgba] = rgba(255, 255, 255, 255), border_radius: int = 20, texture: Union[None, Texture] = None, outlineTexture: Union[None, Texture] = None, scaled: bool = True, scaledOutline: bool = True, transparency: int = 255, transparencyOutline: int = 255, rotation: int = 0) -> None
drawHitbox(window, color: Union[rgb, rgba] = rgba(150, 0, 0, 255)) -> None

use:
  def test():
    gaphcis.drawRect(window, gaphcis.vec2(35, 35), 70, 70, gaphcis.rgb(250, 250, 250))
    gaphcis.drawRect(window, gaphcis.vec2(35, 35), 70, 70, gaphcis.rgb(0, 150, 0), lineDepth=5)
    gaphcis.drawCircle(window, gaphcis.vec2(400, 170), 70, gaphcis.rgb(150,0,0), gaphcis.Texture("./test.jpg"), scaled=False)
    gaphcis.drawTriangle(window, gaphcis.vec2(200, 170), 70, 70, gaphcis.rgb(0, 0, 150), gaphcis.Texture("./test.jpg"))

  test_button = gaphics.Button(70, 30, gaphcis.vec2(250, 125), "test", test)
  graphics.addButton(test_button)
  ...
  gameLoop():
    ...
    test_button.draw(window, 0, "Arial", g.rgb(0, 0, 0), True, 2, g.rgb(250,200,250), g.rgb(0,0,150)) 
    ...
