from collections.abc import Callable
from typing import List, Tuple, Dict
from functools import reduce
from dataclasses import dataclass, field
import pygame as pg
import time
import threading
from math import sqrt
import sys

__all__ = ["vec2", "rgb", "rgba", "Timer", "Button", "InputListener", "Surface", "Window", "init", "quit"]

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

mouse_buttons = {
        pg.BUTTON_LEFT: "LEFT",
        pg.BUTTON_RIGHT: "RIGHT",
        pg.BUTTON_MIDDLE: "MIDDLE",
        pg.BUTTON_WHEELUP: "WHEEL UP",
        pg.BUTTON_WHEELDOWN: "WHEEL DOWN"
}

ScrollDIR = {
        "UP": False,
        "DOWN": False
}

@dataclass(frozen=True, eq=True)
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
        return vec2(0, 0)

    def _get(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
    def __mul__(self, factor: int) -> 'vec2':
        return vec2(self.x * factor, self.y * factor)
    
    def __add__(self, other: 'vec2') -> 'vec2':
        return vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'vec2') -> 'vec2':
        return vec2(self.x - other.x, self.y - other.y)
    
    def dot(self, other: 'vec2') -> int:
        return self.x*other.x + self.y*other.y
    
    def norm(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def normalized(self) -> Tuple[float, float]:
        magnitude = self.norm()
        if magnitude == 0:
            return 0, 0
        else:
            return self.x / magnitude, self.y / magnitude

@dataclass(frozen=True, eq=True)
class rgba:
    red: int
    green: int
    blue: int
    alpha: int

    def __post_init__(self) -> None:
        if self.red > 255 or self.red < 0:
            raise IndexError("Red value out of range. Range: 0..255")
        if self.green > 255 or self.green < 0:
            raise IndexError("Green value out of range. Range: 0..255")
        if self.blue > 255 or self.blue < 0:
            raise IndexError("Blue value out of range. Range: 0..255")
        if self.alpha > 255 or self.alpha < 0:
            raise IndexError("Alpha value out of range. Range: 0..255")

    def _get(self) -> Tuple[int, int, int, int]:
        return (self.red, self.green, self.blue, self.alpha)

@dataclass(frozen=True, eq=True)
class rgb:
    red: int
    green: int
    blue: int

    def __post_init__(self) -> None:
        if self.red > 255 or self.red < 0:
            raise IndexError("Red value out of range. Range: 0..255")
        if self.green > 255 or self.green < 0:
            raise IndexError("Green value out of range. Range: 0..255")
        if self.blue > 255 or self.blue < 0:
            raise IndexError("Blue value out of range. Range: 0..255")

    def _get(self) -> Tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    def getRGBA(self, alpha: int = 255) -> rgba:
        return rgba(self.red, self.green, self.blue, alpha)

class Timer:
    def __init__(self, delay: int, task: Callable) -> None:
        self.delay = delay
        self.task = task
        self.running = False
        self.paused = False
        self.thread = None
        self.stop_flag = threading.Event()

    def _run(self) -> None:
        last_update: int = pg.time.get_ticks()
        while self.running and pg.get_init() and not self.stop_flag.is_set():
            current_time = pg.time.get_ticks()
            if current_time - last_update >= self.delay:
                last_update = current_time
                if not self.paused:
                    self.task()
            time.sleep(0.01)

    def start(self) -> None:
        if not self.running:
            self.running = True
            self.stop_flag.clear()
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def pause(self) -> None:
        if self.running:
            self.paused = True

    def unpause(self) -> None:
        if self.paused:
            self.paused = False

    def stop(self) -> None:
        if self.running and self.thread:
            self.stop_flag.set()
            self.thread.join()
            self.running = False

@dataclass(frozen=True, eq=True)
class Texture:
    filePath: str
    texture: pg.Surface = field(compare=False, init=False)
    original: pg.Surface = field(compare=False, init=False)
    loaded: Dict[Tuple[bool, vec2 | None, int | None, int | None], pg.Surface | None] = field(compare=False, init=False)
    
    def __post_init__(self) -> None:
        object.__setattr__(self, 'loaded', {})

    def load(self) -> None:
        try:
            object.__setattr__(self, 'original', pg.image.load(self.filePath))
            object.__setattr__(self, 'texture', self.original)
        except pg.error as e:
            print(f"Error loading texture: {e}")
            sys.exit()
            
    def __load_tileTexture__(self, width: int = None, height: int = None) -> None:
        width = width or self.texture.get_width()
        height = height or self.texture.get_height()
        
        result = pg.Surface((width, height), pg.SRCALPHA)
        for x in range(0, width, self.texture.get_width()):
            for y in range(0, height, self.texture.get_height()):
                result.blit(self.texture, (x, y))
        object.__setattr__(self, 'texture', result)
        
    def __load_texturePart__(self, start: vec2 = vec2(0, 0), width: int = None, height: int = None) -> None:
        width = width or self.texture.get_width()
        height = height or self.texture.get_height()
        
        if not (0 <= start.x < self.texture.get_width() and 0 <= start.y < self.texture.get_height()):
            raise IndexError("Starting position is out of range")

        result = pg.Surface((width, height), pg.SRCALPHA)
        
        source_rect = pg.Rect(start.x, start.y, width, height)
        result.blit(self.texture, (0, 0), source_rect)
        
        object.__setattr__(self, 'texture', result)
            
    def reset(self) -> None:
        object.__setattr__(self, 'texture', self.original)

    def convert(self, width: int, height: int, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None) -> None:
        if not self.loaded.get((scaled, starting_point, part_width, part_height), None):
            if scaled:
                if starting_point:
                    self.__load_texturePart__(starting_point, (self.texture.get_width() - starting_point.x) - 1, (self.texture.get_height() - starting_point.y) - 1)
                    object.__setattr__(self, 'texture', self.getScaled(width, height))
                else:
                    object.__setattr__(self, 'texture', self.getScaled(width, height))
            else:
                if not starting_point:
                    self.__load_tileTexture__(width, height)
                else:
                    if part_width and part_height:
                        self.__load_texturePart__(starting_point, part_width, part_height)
                        object.__setattr__(self, 'texture', self.getScaled(width, height))
                    else:
                        raise TypeError("Missing arguments part_width, part_height")
            self.loaded[(scaled, starting_point, part_width, part_height)] = self.texture
        else:
            object.__setattr__(self, 'texture', self.loaded[(scaled, starting_point, part_width, part_height)])
            object.__setattr__(self, 'texture', self.getScaled(width, height))
        

    def apply_alpha(self, mask: pg.Surface, transparency: float | int = 255) -> pg.Surface:
        texture = self.texture.convert_alpha()
        target = pg.surfarray.pixels_alpha(texture)
        mask.set_alpha(0)
        target_array = pg.surfarray.array2d(mask) * (1 / (transparency * 255))
        target[:] = target_array
        del target
        return texture
    
    def apply(self, window: pg.Surface, mask: pg.Surface, topleft: vec2, transparency) -> None:
        window.blit(self.apply_alpha(mask, transparency), topleft._get())

    def set_colorkey(self, color: rgb) -> None:
        self.texture.set_colorkey(color._get())

    def rotate(self, rotation: int) -> None:
        if self.texture:
            object.__setattr__(self, 'texture', pg.transform.rotate(self.texture, -rotation))

    def getScaled(self, width: int, height: int) -> pg.Surface:
        return pg.transform.scale(self.texture, (width, height))

    def get(self) -> pg.Surface:
        return self.texture
    
def getFontSize(text: str, font_style: None | str, width: int, height: int) -> int:
    font_size = 1
    font = pg.font.Font(pg.font.match_font(font_style), font_size) if font_style else pg.font.Font(None, font_size)
    text_surface = font.render(text, False, (0, 0, 0, 0))

    # Perform binary search to find optimal font size
    low, high = 1, max(width, height)
    while low <= high:
        mid = (low + high) // 2
        font = pg.font.Font(pg.font.match_font(font_style), mid) if font_style else pg.font.Font(None, mid)
        text_surface = font.render(text, False, (0, 0, 0, 0))
        
        if text_surface.get_width() <= width and text_surface.get_height() <= height:
            font_size = mid
            low = mid + 1
        else:
            high = mid - 1

    del font

    return font_size

@dataclass(frozen=True, eq=True)
class Text:
    text: str
    style: None | str = None
    text_surface: pg.Surface = field(init=False, compare=False)
    loaded: bool = field(init=False, compare=False, default=False)

    def load(self, width: int, height: int, color: rgb | rgba) -> None:
        if not self.loaded:
            font_size = getFontSize(self.text, self.style, width, height)
            font = pg.font.Font(pg.font.match_font(self.style), font_size) if self.style else pg.font.Font(None, font_size)
            object.__setattr__(self, 'text_surface', font.render(self.text, False, color._get()))
            object.__setattr__(self, 'loaded', True)

    def set_alpha(self, alpha: int = 255) -> None:
        self.text_surface.set_alpha(alpha)

    def rotate(self, rotation: int = 0) -> None:
        object.__setattr__(self, 'text_surface', pg.transform.rotate(self.text_surface, -rotation))

    def size(self) -> Tuple[int, int]:
        return self.text_surface.get_size()

    def get(self, width: int, height: int) -> pg.Surface:
        return pg.transform.scale(self.text_surface, (width, height))
    
class Button:
    def __init__(self, width: int, height: int, pos: vec2, label: None | str, runOnClick: Callable) -> None:
        topleft = pos.convert(width, height, "tl")
        bottomright = pos.convert(width, height, "br")
        self.range = pg.Rect(topleft.x, topleft.y, bottomright.x - topleft.x, bottomright.y - topleft.y)
        self.width = width
        self.height = height
        self.pos = pos
        self.topx = topleft.x
        self.topy = topleft.y
        self.label = label
        self.runOnClick = runOnClick
        self.isDrawn: bool = False

    def _onClick(self, pos: vec2) -> None:
        if self.range.collidepoint(*pos._get()):
            self.runOnClick()

    def draw(self, window: 'Window', design: int = 0, fontStyle: str | None = None, fontColor: rgb = rgb(0, 0, 0), outlined: bool = False, outline_depth: int = 0, color: rgb | rgba = rgba(255, 255, 255, 255), outlineColor: rgb | rgba = rgba(255, 255, 255, 255), border_radius: int = 20, texture: None | str = None, outlineTexture: None | str = None, transparency: int = 255, transparencyOutline: int = 255, rotation: int = 0) -> None:
        self.isDrawn = True
        if design == 0:
            window.drawRect(self.pos, self.width, self.height, color, texture, transparency=transparency, rotation=rotation)
            if outlined:
                window.drawRect(self.pos, self.width, self.height, outlineColor, outlineTexture, transparency=transparencyOutline, rotation=rotation, lineDepth=outline_depth)
        elif design == 1:
            window.drawRect(self.pos, self.width, self.height, color, texture, transparency=transparency, rotation=rotation, border_radius=border_radius)
            if outlined:
                window.drawRect(self.pos, self.width, self.height, outlineColor, outlineTexture, transparency=transparencyOutline, rotation=rotation, border_radius=border_radius, lineDepth=outline_depth)
        if self.label != None:
            window.drawText(self.pos, self.width, self.height - ((self.height // 2) // 4), self.label, fontColor, fontStyle, rotation=rotation, transparency=transparency)

    def _drawHitbox(self, screen: pg.Surface, color: rgb | rgba = rgba(150, 0 ,0, 255)) -> None:
        pg.draw.rect(screen, color._get(), (self.topx, self.topy, self.width, self.height), 1)

class InputListener:
    def __init__(self) -> None:
        self.keys_down: Dict[str, bool] = { key_name: False for key_name in keys.values() }
        self.just_pressed_keys: List[str] = []
        self.just_released_keys: List[str] = []

        self.Mouse_Moved: bool = False
        self.ScrollSpeed: int = 0
        self.ScrollDIR: Dict[str, bool] = ScrollDIR.copy()

        self.buttons_down: Dict[str, bool] = { button_name: False for button_name in mouse_buttons.values() }
        self.just_pressed_buttons: List[str] = []
        self.just_released_buttons: List[str] = []

        self.isPressed: None | Callable[[str], None] = None
        self.wasPressed: None | Callable[[str], None] = None
        self.wasReleased: None | Callable[[str], None] = None


    def set_wasPressed(self, function: Callable[[str], None]) -> None:
        self.wasPressed = function

    def set_wasReleased(self, function: Callable[[str], None]) -> None:
        self.wasReleased = function

    def set_isPressed(self, function: Callable[[str], None]) -> None:
        self.isPressed = function

    def _set_key(self, key: str, isPressed: bool) -> None:
        self.keys_down[key] = isPressed
        if isPressed:
            self.just_pressed_keys.append(key)
        else:
            self.just_released_keys.append(key)

    def _set_button(self, button: str, isPressed: bool) -> None:
        self.buttons_down[button] = isPressed
        if isPressed:
            self.just_pressed_buttons.append(button)
        else:
            self.just_released_buttons.append(button)

    def _set_dir(self, dir: str, isDir: bool) -> None:
        self.ScrollDIR[dir] = isDir
    
    def _set_mouse_moved(self, hasMoved: bool) -> None:
        self.Mouse_Moved = hasMoved

    def _set_scroll_speed(self, speed: int) -> None:
        self.ScrollSpeed = speed

    def _call(self) -> None:
        for key in self.keys_down:
            if key:
                if self.isPressed:
                    self.isPressed(key)

        for button in self.buttons_down:
            if button:
                if self.isPressed:
                    self.isPressed(button)

    def _call_wasPressed(self, key: str) -> None:
        if self.wasPressed:
            self.wasPressed(key)

    def _call_wasReleased(self, key: str) -> None:
        if self.wasReleased: 
            self.wasReleased(key)

    def _clear(self) -> None:
        self.just_pressed_keys.clear()
        self.just_released_keys.clear()
        self.just_pressed_buttons.clear()
        self.just_released_buttons.clear()

    def isKeyPressed(self, key: str) -> bool:
        return self.keys_down.get(key, False)

    def wasKeyPressed(self, key: str) -> bool:
        if key in self.just_pressed_keys:
            return True
        return False

    def wasKeyReleased(self, key: str) -> bool:
        if key in self.just_released_keys:
            return True
        return False

    def isButtonPressed(self, button: str) -> bool:
        return self.buttons_down.get(button, False)

    def wasButtonPressed(self, button: str) -> bool:
        if button in self.just_pressed_buttons:
            return True
        return False

    def wasButtonReleased(self, button: str) -> bool:
        if button in self.just_released_buttons:
            return True
        return False

    def isScrollDir(self, dir: str) -> bool:
        return self.ScrollDIR.get(dir, False)

    def getScrollSpeed(self) -> int:
        return self.ScrollSpeed

    def hasMouseMoved(self) -> bool:
        return self.Mouse_Moved

initialized_texts: List[Text] = []
initialized_textures: List[Texture] = []

class Surface:
    def __init__(self, width: int, height: int) -> None:
        self.surf: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        self.ClearColor: rgb | rgba = rgba(0, 0, 0, 0)

    def setClearColor(self, color: rgb | rgba) -> None:
        self.ClearColor = color

    def clear(self):
        self.surf.fill(self.ClearColor._get())

    def set_colorkey(self, colorkey: rgb) -> None:
        self.surf.set_colorkey(colorkey._get())

    def set_alpha(self, alpha: int) -> None:
        self.surf.set_alpha(alpha)

    def drawLine(self, pos1: vec2, pos2: vec2, color: rgb | rgba = rgba(255, 255, 255, 255), depth: int = 1) -> None:
        pg.draw.line(self.surf, color._get(), pos1._get(), pos2._get(), depth)

    def drawRect(self, pos: vec2, width: int, height: int, color: rgb | rgba = rgba(255, 255, 255, 255), texturePath: None | str = None, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, lineDepth: int = 0, rotation: int = 0, transparency: int = 255, border_radius: int = 0) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.rect(mask, color._get(), (0, 0, width, height), lineDepth, border_radius)
        mask.set_alpha(transparency)

        mask = pg.transform.rotate(mask, -rotation)

        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            texture.convert(width, height, scaled, starting_point, part_width, part_height)
            texture.rotate(rotation)
            if colorkey:
                texture.set_colorkey(colorkey)
            texture.apply(self.surf, mask, topleft, transparency)
            texture.reset()
        else:
            self.surf.blit(mask, topleft._get())

    def drawCircle(self, pos: vec2, radius: int, color: rgb | rgba = rgba(255, 255, 255, 255), texturePath: None | str = None, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(radius * 2, radius * 2, "tl")
        mask: pg.Surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(mask, color._get(), (radius, radius), radius, lineDepth)
        mask.set_alpha(transparency)

        mask = pg.transform.rotate(mask, -rotation)

        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            texture.convert(radius*2, radius*2, scaled, starting_point, part_width, part_height)
            texture.rotate(rotation)
            if colorkey:
                texture.set_colorkey(colorkey)
            texture.apply(self.surf, mask, topleft, transparency)
            texture.reset()
        else:
            self.surf.blit(mask, topleft._get())

    def drawTriangle(self, pos: vec2, width: int, height: int, color: rgb | rgba = rgba(255, 255, 255, 255), texturePath: None | str = None, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.polygon(mask, color._get(), [((width//2) - 2, 0), (0, height - 2), (width - 2, height - 2)], lineDepth)
        mask.set_alpha(transparency)

        mask = pg.transform.rotate(mask, -rotation)

        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            texture.convert(width, height, scaled, starting_point, part_width, part_height)
            texture.rotate(rotation)
            if colorkey:
                texture.set_colorkey(colorkey)
            texture.apply(self.surf, mask, topleft, transparency)
            texture.reset()
        else:
            self.surf.blit(mask, topleft._get())
        
    def drawTexture(self, pos: vec2, width: int, height: int, texturePath: str, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        texture = Texture(texturePath)
        if not texture in initialized_textures:
            texture.load()
            initialized_textures.append(texture)
        else:
            filtered = list(filter(lambda x: x == texture, initialized_textures))
            texture = filtered[-1]
        texture.convert(width, height, scaled, starting_point, part_width, part_height)
        texture.rotate(rotation)
        if colorkey:
            texture.set_colorkey(colorkey)
        texture.apply(self.surf, self.surf, topleft, transparency)
        texture.reset()

    def drawText(self, pos: vec2, width: int, height: int, text: str, color: rgb | rgba = rgba(0, 0, 0, 255), fontStyle: None | str = None, *, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_texts
        topleft: vec2 = pos.convert(width, height, "tl")
        text_instance: Text = Text(text, fontStyle)
        if not text_instance in initialized_texts:
            text_instance.load(self.surf.get_width(), self.surf.get_height(), color)
            initialized_texts.append(text_instance)
        else:
            filtered = list(filter(lambda x: x == text_instance, initialized_texts))
            text_instance = filtered[-1]
        text_instance.set_alpha(transparency)
        text_instance.rotate(rotation)
        self.surf.blit(text_instance.get(width - ((width // 2) // 4), height - ((height // 2) // 4)), vec2(topleft.x + ((width // 2) // 4) // 2, topleft.y + ((height // 2) // 4) // 2)._get())

    def drawSurface(self, topleft: vec2, surface: 'Surface') -> None:
        self.surf.blit(surface._get(), topleft._get())
        
    def _get(self) -> pg.Surface:
        return self.surf

class Window:
    def __init__(self, width: int, height: int, caption: str, caption_icon: str = "none", window_flags: List[int] = []) -> None:
        flags = reduce(lambda x, y: x | y, window_flags) if len(window_flags) > 0 else 0
        self.screen: pg.Surface = pg.display.set_mode((width, height), flags)
        pg.display.set_caption(caption)
        if caption_icon != "none":
            pg.display.set_icon(pg.image.load(caption_icon))
        self.db = False
        if pg.DOUBLEBUF in window_flags:
            self.db = True

        self.clock = pg.time.Clock()
        self.running: bool = False

        self.ClearColor: rgb = rgb(0, 0, 0)
        
        self.hitboxColor: rgb | rgba = rgb(0,0,0)
        self.drawHitboxes: bool = False

        self.visual_buttons: List[Button] = []

        self.escape_sequence: Tuple[str, ...] | str = "ESCAPE"
        self.framerate: int = 60

        self.current: int = 0
        self.last_time: int = 0
        self.last_update: int = 0
        self.fps: float = 0
    
    def getDeltaTime(self) -> float:
        return (self.current - self.last_time) / 1000
    
    def getTimeDiff(self) -> float:
        return(self.current - self.last_update) / 1000

    def getFPS(self) -> int:
        return int(self.fps)
    
    def getLiteralFPS(self) -> float:
        return self.fps
    
    def setFrameRate(self, rate: int) -> None:
        self.framerate = rate

    def drawLine(self, pos1: vec2, pos2: vec2, color: rgb | rgba = rgba(255, 255, 255, 255), depth: int = 1) -> None:
        pg.draw.line(self.screen, color._get(), pos1._get(), pos2._get(), depth)

    def drawRect(self, pos: vec2, width: int, height: int, color: rgb | rgba = rgba(255, 255, 255, 255), texturePath: None | str = None, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, lineDepth: int = 0, rotation: int = 0, transparency: int = 255, border_radius: int = 0) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.rect(mask, color._get(), (0, 0, width, height), lineDepth, border_radius)
        mask.set_alpha(transparency)

        mask = pg.transform.rotate(mask, -rotation)

        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            texture.convert(width, height, scaled, starting_point, part_width, part_height)
            texture.rotate(rotation)
            if colorkey:
                texture.set_colorkey(colorkey)
            texture.apply(self.screen, mask, topleft, transparency)
            texture.reset()
        else:
            self.screen.blit(mask, topleft._get())

    def drawCircle(self, pos: vec2, radius: int, color: rgb | rgba = rgba(255, 255, 255, 255), texturePath: None | str = None, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(radius * 2, radius * 2, "tl")
        mask: pg.Surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(mask, color._get(), (radius, radius), radius, lineDepth)
        mask.set_alpha(transparency)

        mask = pg.transform.rotate(mask, -rotation)

        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            texture.convert(radius*2, radius*2, scaled, starting_point, part_width, part_height)
            texture.rotate(rotation)
            if colorkey:
                texture.set_colorkey(colorkey)
            texture.apply(self.screen, mask, topleft, transparency)
            texture.reset()
        else:
            self.screen.blit(mask, topleft._get())

    def drawTriangle(self, pos: vec2, width: int, height: int, color: rgb | rgba = rgba(255, 255, 255, 255), texturePath: None | str = None, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.polygon(mask, color._get(), [((width//2) - 2, 0), (0, height - 2), (width - 2, height - 2)], lineDepth)
        mask.set_alpha(transparency)

        mask = pg.transform.rotate(mask, -rotation)

        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            texture.convert(width, height, scaled, starting_point, part_width, part_height)
            texture.rotate(rotation)
            if colorkey:
                texture.set_colorkey(colorkey)
            texture.apply(self.screen, mask, topleft, transparency)
            texture.reset()
        else:
            self.screen.blit(mask, topleft._get())
        
    def drawTexture(self, pos: vec2, width: int, height: int, texturePath: str, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        texture = Texture(texturePath)
        if not texture in initialized_textures:
            texture.load()
            initialized_textures.append(texture)
        else:
            filtered = list(filter(lambda x: x == texture, initialized_textures))
            texture = filtered[-1]
        texture.convert(width, height, scaled, starting_point, part_width, part_height)
        texture.rotate(rotation)
        if colorkey:
            texture.set_colorkey(colorkey)
        texture.apply(self.screen, self.screen, topleft, transparency)
        texture.reset()

    def drawText(self, pos: vec2, width: int, height: int, text: str, color: rgb | rgba = rgba(0, 0, 0, 255), fontStyle: None | str = None, *, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_texts
        topleft: vec2 = pos.convert(width, height, "tl")
        text_instance: Text = Text(text, fontStyle)
        if not text_instance in initialized_texts:
            text_instance.load(self.screen.get_width(), self.screen.get_height(), color)
            initialized_texts.append(text_instance)
        else:
            filtered = list(filter(lambda x: x == text_instance, initialized_texts))
            text_instance = filtered[-1]
        text_instance.set_alpha(transparency)
        text_instance.rotate(rotation)
        self.screen.blit(text_instance.get(width - ((width // 2) // 4), height - ((height // 2) // 4)), vec2(topleft.x + ((width // 2) // 4) // 2, topleft.y + ((height // 2) // 4) // 2)._get())

    def drawSurface(self, topleft: vec2, surface: 'Surface') -> None:
        self.screen.blit(surface._get(), topleft._get())

    def getMousePos(self) -> vec2:
        return vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

    def addButton(self, button: Button) -> None :
        self.visual_buttons.append(button)

    def setClearColor(self, color: rgb) -> None:
        self.ClearColor = color

    def get_width(self) -> int:
        return self.screen.get_width()
    
    def get_height(self) -> int:
        return self.screen.get_height()
    
    def get_size(self) -> Tuple[int, int]:
        return self.screen.get_width(), self.screen.get_height()

    def clear(self) -> None:
        self.screen.fill(self.ClearColor._get())

    def startGameLoop(self, gameLoop: Callable, escape_sequence: Tuple[str, ...] | str, framerate: int, input: None | InputListener = None) -> None:
        self.escape_sequence = escape_sequence
        self.framerate = framerate

        self.running = True

        while self.running:

            self.current = pg.time.get_ticks()
            self.last_time = self.current

            if input:
                input._clear()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if input:
                    if event.type == pg.KEYDOWN:
                        if event.key in keys:
                            input._set_key(keys[event.key], True)
                            input._call_wasPressed(keys[event.key])
                    escape = False
                    if isinstance(escape_sequence, str):
                        escape = input.isKeyPressed(escape_sequence)     
                    else:
                        escape = all(input.isKeyPressed(key) for key in escape_sequence)    
                    if escape:
                        self.running = False
                    elif event.type == pg.KEYUP:
                        if event.key in keys:
                            input._set_key(keys[event.key], False)
                            input._call_wasReleased(keys[event.key])
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if event.button in mouse_buttons:
                            input._set_button(mouse_buttons[event.button], True)
                    elif event.type == pg.MOUSEBUTTONUP:
                        if event.button in mouse_buttons:
                            input._set_button(mouse_buttons[event.button], False)
                    if event.type == pg.MOUSEWHEEL:
                        input._set_scroll_speed(event.y)
                        if event.y > 0:
                            input._set_dir("UP", True)
                            input._set_dir("DOWN", False)
                        elif event.y < 0: 
                            input._set_dir("UP", True)
                            input._set_dir("DOWN", False)
                    else:
                        input._set_scroll_speed(0)
                    if event.type == pg.MOUSEMOTION:
                        input._set_mouse_moved(True)
                    else:
                        input._set_mouse_moved(True)

                    if input.getScrollSpeed():
                        input._set_dir("UP", False)
                        input._set_dir("DOWN", False)

            input._call()    

            if not self.running:
                break     

            for button in self.visual_buttons:
                button.isDrawn = False       
            
            gameLoop()

            if self.drawHitboxes:
                for button in self.visual_buttons:
                    if button.isDrawn:
                        button._drawHitbox(self.screen, self.hitboxColor)
            
            if input:
                if input.wasButtonPressed("LEFT"):
                    for button in self.visual_buttons:
                        if button.isDrawn:
                            button._onClick(self.getMousePos())

            if self.getTimeDiff() >= 1:
                self.fps = self.clock.get_fps()
                self.last_update = self.current

            pg.display.update() if not self.db else pg.display.flip()
            self.clock.tick(self.framerate)

    def quit(self) -> None:
        if self.running:
            self.running = False

initialized: bool = False

def init() -> None:
    global initialized
    if not initialized:
        if not pg.get_init():
            pg.init()
            initialized = True

def quit() -> None:
    global initialized
    if initialized:
        pg.quit()
        sys.exit()
