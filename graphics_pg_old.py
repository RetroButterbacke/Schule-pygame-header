from collections.abc import Callable
from typing import List, Tuple, Union
from dataclasses import dataclass
import pygame as pg
from pygame.time import Clock 
import sys
import threading
import time
from math import sqrt

clock = Clock()
running: bool = False

keys = {
    pg.K_a: "A",
    pg.K_b: "B",
    pg.K_c: "C",
    pg.K_d: "D",
    pg.K_e: "E",
    pg.K_f: "F", 
    pg.K_g: "G",
    pg.K_h: "H",
    pg.K_i: "I",
    pg.K_j: "J",
    pg.K_k: "K",
    pg.K_l: "L",
    pg.K_m: "M",
    pg.K_n: "N",
    pg.K_o: "O",
    pg.K_p: "P",
    pg.K_q: "Q",
    pg.K_r: "R",
    pg.K_s: "S",
    pg.K_t: "T",
    pg.K_u: "U",
    pg.K_v: "V",
    pg.K_w: "W",
    pg.K_x: "X",
    pg.K_y: "Y",
    pg.K_z: "Z",

    pg.K_0: "0",
    pg.K_1: "1",
    pg.K_2: "2",
    pg.K_3: "3",
    pg.K_4: "4",
    pg.K_5: "5",
    pg.K_6: "6",
    pg.K_7: "7",
    pg.K_8: "8",
    pg.K_9: "9",

    pg.K_RETURN: "RETURN",
    pg.K_ESCAPE: "ESCAPE",
    pg.K_BACKSPACE: "BACKSPACE",
    pg.K_TAB: "TAB",
    pg.K_SPACE: "SPACE",

    pg.K_UP: "UP",
    pg.K_DOWN: "DOWN",
    pg.K_LEFT: "LEFT",
    pg.K_RIGHT: "RIGHT",

    pg.K_LCTRL: "LEFT CTRL",
    pg.K_RCTRL: "RIGHT CTRL",
    pg.K_LSHIFT: "LEFT SHIFT",
    pg.K_RSHIFT: "RIGHT SHIFT",
    pg.K_LALT: "LEFT ALT",
    pg.K_RALT: "RIGHT ALT",

    pg.K_KP0: "KP_0",
    pg.K_KP1: "KP_1",
    pg.K_KP2: "KP_2",
    pg.K_KP3: "KP_3",
    pg.K_KP4: "KP_4",
    pg.K_KP5: "KP_5",
    pg.K_KP6: "KP_6",
    pg.K_KP7: "KP_7",
    pg.K_KP8: "KP_8",
    pg.K_KP9: "KP_9",
    pg.K_KP_ENTER: "KEYPAD ENTER",
    pg.K_KP_PLUS: "KEYPAD PLUS",
    pg.K_KP_MINUS: "KEYPAD MINUS",
    pg.K_KP_MULTIPLY: "KEYPAD MULTIPLY",
    pg.K_KP_DIVIDE: "KEYPAD DIVIDE",

    pg.K_F1: "F1",
    pg.K_F2: "F2",
    pg.K_F3: "F3",
    pg.K_F4: "F4",
    pg.K_F5: "F5",
    pg.K_F6: "F6",
    pg.K_F7: "F7",
    pg.K_F8: "F8",
    pg.K_F9: "F9",
    pg.K_F10: "F10",
    pg.K_F11: "F11",
    pg.K_F12: "F12",
}

keys_down = { key_name: False for key_name in keys.values() }
just_pressed_keys: List[str] = []
just_released_keys: List[str] = []

Mouse_Moved = False
ScrollSpeed = 0

ScrollDIR = {
        "UP": False,
        "DOWN": False
}

mouse_buttons = {
        pg.BUTTON_LEFT: "LEFT",
        pg.BUTTON_RIGHT: "RIGHT",
        pg.BUTTON_MIDDLE: "MIDDLE",
        pg.BUTTON_WHEELUP: "WHEEL UP",
        pg.BUTTON_WHEELDOWN: "WHEEL DOWN"
}

buttons_down = { button_name: False for button_name in mouse_buttons.values() }
just_pressed_buttons: List[str] = []
just_released_buttons: List[str] = []

@dataclass
class vec2:
    x: int
    y: int

    def convert(self, width: int, height: int, modifier: str) -> 'vec2':
        if modifier == "ctl":
            return vec2(self.x + width//2, self.y + height//2)
        if modifier == "ctr":
            return vec2(self.x - width//2, self.y + height//2)
        if modifier == "cbl":
            return vec2(self.x + width//2, self.y - height//2)
        if modifier == "cbr":
            return vec2(self.x - width//2, self.y - height//2)
        elif modifier == "tl":
            return vec2(self.x - width//2, self.y - height//2)
        elif modifier == "tr":
            return vec2(self.x + width//2, self.y - height//2)
        elif modifier == "bl":
            return vec2(self.x - width//2, self.y + height//2)
        elif modifier == "br":
            return vec2(self.x + width//2, self.y + height//2)

    def get(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other: 'vec2') -> bool:
            return self.x == other.x and self.y == other.y
    
    def __mul__(self, other: 'vec2') -> int:
        return self.x * other.x + self.y * other.y
    
    def __add__(self, other: 'vec2') -> 'vec2':
        return vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'vec2') -> 'vec2':
        return vec2(self.x - other.x, self.y - other.y)
    
    def norm(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def normalized(self) -> 'vec2':
        magnitude = self.norm()
        if magnitude == 0:
            return vec2(0, 0)
        else:
            return vec2(self.x / magnitude, self.y / magnitude)

@dataclass
class rgba:
    red: int
    green: int
    blue: int
    alpha: int

    def get(self) -> Tuple[int, int, int, int]:
        if self.alpha > 255 or self.alpha < 0:
            raise IndexError("Alpha value out of range. Range: 0..255")
        return (self.red, self.green, self.blue, self.alpha)

@dataclass
class rgb:
    red: int
    green: int
    blue: int

    def get(self) -> Tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    def getRGBA(self, alpha: int = 255) -> rgba:
        return rgba(self.red, self.green, self.blue, alpha)

class Timer:
    def __init__(self, delay: int, task: Callable):
        self.delay = delay
        self.task = task
        self.running = False
        self.thread = None
        self.stop_flag = threading.Event()

    def _run(self):
        global running
        last_update: int = pg.time.get_ticks()
        while self.running and running and not self.stop_flag.is_set():
            current_time = pg.time.get_ticks()
            if current_time - last_update >= self.delay:
                last_update = current_time
                self.task()
            time.sleep(0.01)

    def start(self) -> None:
        if not self.running:
            self.running = True
            self.stop_flag.clear()
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        if self.running:
            self.stop_flag.set()
            self.thread.join()
            self.running = False

class Texture:
    def __init__(self, filePath: str):
        try:
            self.image = pg.image.load(filePath)
        except pg.error as e:
            print(f"Error loading texture: {e}")
            sys.exit()

    def convert(self, width: int, height: int, scaled: bool) -> None:
        self.texture: pg.Surface = self.getScaled(width, height) if scaled else self.get()

    # the higher the transparency, the more you can see it max 3.9.....(< 4) for 8-bit because 32 bits are to high for this?! for 16 bit its 14  wich would be polygons
    def apply_alpha(self, mask: pg.Surface, transparency: float | int = 3.9999999) -> pg.Surface:
        texture = self.texture.convert_alpha()
        target = pg.surfarray.pixels_alpha(texture)
        target_array = pg.surfarray.array2d(mask) * transparency
        target[:] = target_array
        del target
        return texture

    def apply(self, window: pg.Surface, mask: pg.Surface, topleft: vec2, transparency) -> None:
        window.blit(self.apply_alpha(mask, transparency), topleft.get())

    def rotate(self, rotation: int) -> None:
        self.texture = pg.transform.rotate(self.image, -rotation)

    def set_alpha(self, alpha: int) -> None:
        self.texture =  self.texture.set_alpha(alpha)

    def getScaled(self, width: int, height: int) -> pg.Surface:
        return pg.transform.scale(self.image, (width, height))

    def get(self) -> pg.Surface:
        return self.image

class Range:
    def __init__(self, p1x: int, p1y: int, p2x: int, p2y: int):
        if p1x < 0 or p1y < 0 or p2x < 0 or p2y < 0:
            raise IndexError(f"Position out of the window's frame")
        self.pos1 = vec2(p1x, p1y)
        self.pos2 = vec2(p2x, p2y)
        
    def inRange(self, pos: vec2) -> bool:
        if pos.x <= self.pos2.x and pos.x >= self.pos1.x and pos.y >= self.pos1.y and pos.y <= self.pos2.y:
            return True
        else:
            return False

def getFontDimensions(text: str, font_style: None | str, width: int, height: int) -> Tuple[int, int, int]:
    font_size = 1
    font = pg.font.Font(pg.font.match_font(font_style), font_size) if font_style else pg.font.Font(None, font_size)
    text_surface = font.render(text, True, (0, 0, 0, 0))

    # Perform binary search to find optimal font size
    low, high = 1, max(width, height)
    while low <= high:
        mid = (low + high) // 2
        font = pg.font.Font(pg.font.match_font(font_style), mid) if font_style else pg.font.Font(None, mid)
        text_surface = font.render(text, True, (0, 0, 0, 0))
        
        if text_surface.get_width() <= width and text_surface.get_height() <= height:
            font_size = mid
            low = mid + 1
        else:
            high = mid - 1

    font = pg.font.Font(pg.font.match_font(font_style), font_size) if font_style else pg.font.Font(None, font_size)
    text_surface = font.render(text, True, (0, 0, 0, 0))
    
    del font

    return font_size, text_surface.get_width(), text_surface.get_height()

ClearColor: rgb = rgb(0, 0, 0)

def init() -> None:
    pg.init()

def isKeyPressed(key: str) -> bool:
    return keys_down.get(key, False)

def wasKeyPressed(key: str) -> bool:
    if key in just_pressed_keys:
        return True
    return False

def wasKeyReleased(key: str) -> bool:
    if key in just_released_keys:
        return True
    return False

def isButtonPressed(button: str) -> bool:
    return buttons_down.get(button, False)

def wasButtonPressed(button: str) -> bool:
    if button in just_pressed_buttons:
        return True
    return False

def wasButtonReleased(button: str) -> bool:
    if button in just_released_buttons:
        return True
    return False

def isScrollDir(dir: str) -> bool:
    return ScrollDIR.get(dir, False)

def getMousePos() -> vec2:
    return vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

def getScrollSpeed() -> int:
    return ScrollSpeed

def hasMouseMoved() -> bool:
    return Mouse_Moved

hitboxColor: rgb | rgba = rgb(0,0,0)
drawHitboxes: bool = False

def setHitboxColor(color: rgb | rgba) -> None:
    global hitboxColor
    hitboxColor = color

def showHitboxes(draw: bool) -> None:
    global drawHitboxes
    drawHitboxes = draw

def drawLine(window: pg.Surface, pos1: vec2, pos2: vec2, color: rgb | rgba = rgba(255, 255, 255, 255), depth: int = 1) -> None:
    pg.draw.line(window, color.get(), pos1.get(), pos2.get(), depth)

def drawRect(window: pg.Surface, pos: vec2, width: int, height: int, color: rgb | rgba = rgba(255, 255, 255, 255), texture: None | Texture = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255, border_radius: int = 0) -> None:
    topleft: vec2 = pos.convert(width, height, "tl")
    mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
    pg.draw.rect(mask, color.get(), (0, 0, width, height), lineDepth, border_radius)
    mask.set_alpha(transparency)

    mask = pg.transform.rotate(mask, -rotation)

    if texture != None:
        texture.rotate(rotation)
        texture.convert(width, height, scaled)
        texture.apply(window, mask, topleft, transparency)
    else:
        window.blit(mask, topleft.get())
            

def drawCircle(window: pg.Surface, pos: vec2, radius: int, color: rgb | rgba = rgba(255, 255, 255, 255), texture: None | Texture = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
    topleft: vec2 = pos.convert(radius * 2, radius * 2, "tl")
    mask: pg.Surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
    pg.draw.circle(mask, color.get(), (radius, radius), radius, lineDepth)
    mask.set_alpha(transparency)

    mask = pg.transform.rotate(mask, -rotation)

    if texture != None:
        texture.rotate(rotation)
        texture.convert(radius * 2, radius * 2, scaled)
        texture.apply(window, mask, topleft, transparency)
    else:
        window.blit(mask, topleft.get())

def drawTriangle(window: pg.Surface, pos: vec2, width: int, height: int, color: rgb | rgba = rgba(255, 255, 255, 255), texture: None | Texture = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
    topleft: vec2 = pos.convert(width, height, "tl")
    mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
    pg.draw.polygon(mask, color.get(), [((width//2) - 2, 0), (0, height - 2), (width - 2, height - 2)], lineDepth)
    mask.set_alpha(transparency)

    mask = pg.transform.rotate(mask, -rotation)

    if texture != None:
        texture.rotate(rotation)
        texture.convert(width, height, scaled)
        texture.apply(window, mask, topleft, transparency)
    else:
        window.blit(mask, topleft.get())

def drawTexture(window: pg.Surface, pos: vec2, width: int, height: int, texture: Texture, *, rotation: int = 0, transparency: int = 255) -> None:
    topleft: vec2 = pos.convert(width, height, "tl")
    texture.rotate(rotation)
    texture.set_alpha(transparency)
    window.blit(texture.getScaled(width, height), topleft.get())

def drawText(window: pg.Surface, pos: vec2, width: int, height: int, text: str, color: rgb | rgba = rgba(0, 0, 0, 255), fontStyle: None | str = None, *, rotation: int = 0, transparency: int = 255) -> None:
    topleft: vec2 = pos.convert(width, height, "tl")
    font_size, text_width, text_height = getFontDimensions(text, fontStyle, width, height)
    font = pg.font.Font(pg.font.match_font(fontStyle), font_size) if fontStyle else pg.font.Font(None, font_size)
    textSurface: pg.Surface = font.render(text, True, color.get())
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    textSurface.set_alpha(transparency)
    textSurface = pg.transform.rotate(textSurface, -rotation)
    textPos: vec2 = vec2(topleft.x + x, topleft.y + y)
    window.blit(textSurface, textPos.get())
    del textSurface
    del font

class Button:
    def __init__(self, width: int, height: int, pos: vec2, label: None | str, runOnClick: Callable):
        topleft = pos.convert(width, height, "tl")
        bottomright = pos.convert(width, height, "br")
        self.range = Range(topleft.x, topleft.y, bottomright.x, bottomright.y)
        self.width = width
        self.height = height
        self.x = topleft.x
        self.y = topleft.y
        self.label = label
        self.runOnClick = runOnClick
        self.isDrawn: bool = False

    def onClick(self, pos: vec2) -> None:
        if self.range.inRange(pos):
            self.runOnClick()

    def draw(self, window: pg.Surface, design: int = 0, fontStyle: str | None = None, fontColor: rgb = rgb(0, 0, 0), outlined: bool = False, outline_depth: int = 0, color: rgb | rgba = rgba(255, 255, 255, 255), outlineColor: rgb | rgba = rgba(255, 255, 255, 255), border_radius: int = 20, texture: None | Texture = None, outlineTexture: None | Texture = None, scaled: bool = True, scaledOutline: bool = True, transparency: int = 255, transparencyOutline: int = 255, rotation: int = 0) -> None:
        self.isDrawn = True
        if design == 0:
            drawRect(window, vec2(self.x, self.y).convert(self.width, self.height, "ctl"), self.width, self.height, color, texture, scaled=scaled, transparency=transparency, rotation=rotation)
            if outlined:
                drawRect(window, vec2(self.x, self.y).convert(self.width, self.height, "ctl"), self.width, self.height, outlineColor, outlineTexture, scaled=scaledOutline, transparency=transparencyOutline, rotation=rotation, lineDepth=outline_depth)
        elif design == 1:
            drawRect(window, vec2(self.x, self.y).convert(self.width, self.height, "ctl"), self.width, self.height, color, texture, scaled=scaled, transparency=transparency, rotation=rotation, border_radius=border_radius)
            if outlined:
                drawRect(window, vec2(self.x, self.y).convert(self.width, self.height, "ctl"), self.width, self.height, outlineColor, outlineTexture, scaled=scaledOutline, transparency=transparencyOutline, rotation=rotation, border_radius=border_radius, lineDepth=outline_depth)
        if self.label != None:
            drawText(window, vec2(self.x, self.y).convert(self.width, self.height, "ctl"), self.width, self.height, self.label, fontColor, fontStyle, rotation=rotation, transparency=transparency)

    def drawHitbox(self, window: pg.Surface, color: rgb | rgba = rgba(150, 0 ,0, 255)) -> None:
        pg.draw.rect(window, color.get(), (self.x, self.y, self.width, self.height), 1)


visual_buttons: List[Button] = []

def addButton(button: Button) -> None :
    global visual_buttons
    visual_buttons.append(button)

def createWindow(width: int, height: int, caption: str, window_flags: int = 0) -> pg.Surface:

    window = pg.display.set_mode((width, height), window_flags)
    pg.display.set_caption(caption)

    return window

def setClearColor(color: rgb) -> None:
    global ClearColor
    ClearColor = color

def startGameLoop(gameLoop: Callable, window: pg.Surface, escape_sequence: Tuple[str, ...] | str, framerate: int)-> None:
    global ScrollSpeed
    global Mouse_Moved
    global just_pressed_keys
    global just_pressed_buttons
    global just_released_keys
    global just_released_buttons
    global running

    running = True

    while running:
        just_pressed_keys.clear()
        just_pressed_buttons.clear()
        just_released_keys.clear()
        just_released_buttons.clear()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key in keys:
                    keys_down[keys[event.key]] = True
                    just_pressed_keys.append(keys[event.key])
                escape = False
                if isinstance(escape_sequence, str):
                    escape = isKeyPressed(escape_sequence)     
                else:
                    escape = all(isKeyPressed(key) for key in escape_sequence)    
                if escape:
                    running = False
            elif event.type == pg.KEYUP:
                if event.key in keys:
                    keys_down[keys[event.key]] = False
                    just_released_keys.append(keys[event.key])
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button in mouse_buttons:
                    buttons_down[mouse_buttons[event.button]] = True
                    just_pressed_buttons.append(mouse_buttons[event.button])
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button in mouse_buttons:
                    buttons_down[mouse_buttons[event.button]] = False
                    just_released_buttons.append(mouse_buttons[event.button])
            if event.type == pg.MOUSEWHEEL:
                ScrollSpeed = event.y
                if event.y > 0:
                    ScrollDIR["UP"] = True
                    ScrollDIR["DOWN"] = False
                elif event.y < 0: 
                    ScrollDIR["UP"] = False
                    ScrollDIR["DOWN"] = True
            else:
                ScrollSpeed = 0
            if event.type == pg.MOUSEMOTION:
                Mouse_Moved = True
            else:
                Mouse_Moved = False

        if ScrollSpeed == 0:
            ScrollDIR["UP"] = False
            ScrollDIR["DOWN"] = False

        if not running:
            break

        window.fill(ClearColor.get())
        
        for button in visual_buttons:
            button.isDrawn = False

        gameLoop()

        if drawHitboxes:
            for button in visual_buttons:
                if button.isDrawn:
                    button.drawHitbox(window, hitboxColor)

        if wasButtonPressed("LEFT"):
            for button in visual_buttons:
                if button.isDrawn:
                    button.onClick(getMousePos())

        pg.display.flip()
        clock.tick(framerate)

    pg.quit()
    return

def quit() -> None:
    global running
    running = False