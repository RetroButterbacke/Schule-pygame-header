from collections.abc import Callable
from typing import List, Tuple, Union, Dict
from dataclasses import dataclass, field
import pygame as pg, pygame
from pygame.time import Clock
import time
import threading
from math import sqrt
import sys

keys = {
    pygame.K_a: "A",
    pygame.K_b: "B",
    pygame.K_c: "C",
    pygame.K_d: "D",
    pygame.K_e: "E",
    pygame.K_f: "F", 
    pygame.K_g: "G",
    pygame.K_h: "H",
    pygame.K_i: "I",
    pygame.K_j: "J",
    pygame.K_k: "K",
    pygame.K_l: "L",
    pygame.K_m: "M",
    pygame.K_n: "N",
    pygame.K_o: "O",
    pygame.K_p: "P",
    pygame.K_q: "Q",
    pygame.K_r: "R",
    pygame.K_s: "S",
    pygame.K_t: "T",
    pygame.K_u: "U",
    pygame.K_v: "V",
    pygame.K_w: "W",
    pygame.K_x: "X",
    pygame.K_y: "Y",
    pygame.K_z: "Z",

    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",

    pygame.K_RETURN: "RETURN",
    pygame.K_ESCAPE: "ESCAPE",
    pygame.K_BACKSPACE: "BACKSPACE",
    pygame.K_TAB: "TAB",
    pygame.K_SPACE: "SPACE",

    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN",
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",

    pygame.K_LCTRL: "LEFT CTRL",
    pygame.K_RCTRL: "RIGHT CTRL",
    pygame.K_LSHIFT: "LEFT SHIFT",
    pygame.K_RSHIFT: "RIGHT SHIFT",
    pygame.K_LALT: "LEFT ALT",
    pygame.K_RALT: "RIGHT ALT",

    pygame.K_KP0: "KP_0",
    pygame.K_KP1: "KP_1",
    pygame.K_KP2: "KP_2",
    pygame.K_KP3: "KP_3",
    pygame.K_KP4: "KP_4",
    pygame.K_KP5: "KP_5",
    pygame.K_KP6: "KP_6",
    pygame.K_KP7: "KP_7",
    pygame.K_KP8: "KP_8",
    pygame.K_KP9: "KP_9",
    pygame.K_KP_ENTER: "KEYPAD ENTER",
    pygame.K_KP_PLUS: "KEYPAD PLUS",
    pygame.K_KP_MINUS: "KEYPAD MINUS",
    pygame.K_KP_MULTIPLY: "KEYPAD MULTIPLY",
    pygame.K_KP_DIVIDE: "KEYPAD DIVIDE",

    pygame.K_F1: "F1",
    pygame.K_F2: "F2",
    pygame.K_F3: "F3",
    pygame.K_F4: "F4",
    pygame.K_F5: "F5",
    pygame.K_F6: "F6",
    pygame.K_F7: "F7",
    pygame.K_F8: "F8",
    pygame.K_F9: "F9",
    pygame.K_F10: "F10",
    pygame.K_F11: "F11",
    pygame.K_F12: "F12",
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

    def get(self) -> Tuple[int, int]:
        return (self.x, self.y)
    
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

    def get(self) -> Tuple[int, int, int, int]:
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

    def get(self) -> Tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    def getRGBA(self, alpha: int = 255) -> rgba:
        return rgba(self.red, self.green, self.blue, alpha)

class Timer:
    def __init__(self, delay: int, task: Callable) -> None:
        self.delay = delay
        self.task = task
        self.running = False
        self.thread = None
        self.stop_flag = threading.Event()

    def _run(self) -> None:
        last_update: int = pg.time.get_ticks()
        while self.running and pg.get_init() and not self.stop_flag.is_set():
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

    def stop(self) -> None:
        if self.running:
            self.stop_flag.set()
            self.thread.join()
            self.running = False

@dataclass(frozen=True, eq=True)
class Texture:
    filePath: str
    texture: pg.Surface = field(compare=False, init=False)
    original: pg.Surface = field(compare=False, init=False)

    def load(self) -> None:
        try:
            object.__setattr__(self, 'original', pg.image.load(self.filePath))
            object.__setattr__(self, 'texture', self.original)
        except pg.error as e:
            print(f"Error loading texture: {e}")
            sys.exit()

    def reset(self) -> None:
        object.__setattr__(self, 'texture', self.original)

    def convert(self, width: int, height: int) -> None:
        object.__setattr__(self, 'texture', self.getScaled(width, height))

    def apply_alpha(self, mask: pg.Surface, transparency: Union[float, int] = 255) -> pg.Surface:
        texture = self.texture.convert_alpha()
        target = pg.surfarray.pixels_alpha(texture)
        mask.set_alpha(0)
        target_array = pg.surfarray.array2d(mask) * (1 / (transparency * 255))
        target[:] = target_array
        del target
        return texture
    
    def apply(self, window: pg.Surface, mask: pg.Surface, topleft: vec2, transparency) -> None:
        window.blit(self.apply_alpha(mask, transparency), topleft.get())

    #def set_colorkey(self, color: Union[rgb, rgba]) -> None:
        #self.texture.set_colorkey(color.get())

    def rotate(self, rotation: int) -> None:
        if self.texture:
            object.__setattr__(self, 'texture', pg.transform.rotate(self.texture, -rotation))

    def set_alpha(self, alpha: int) -> None:
        if self.texture:
            object.__setattr__(self, 'texture', self.texture.set_alpha(alpha))

    def getScaled(self, width: int, height: int) -> pg.Surface:
        return pg.transform.scale(self.texture, (width, height))

    def get(self) -> pg.Surface:
        return self.texture
    
def getFontDimensions(text: str, font_style: Union[None, str], width: int, height: int) -> int:
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
    style: str
    text_surface: pg.Surface = field(init=False, compare=False)
    loaded: bool = field(init=False, compare=False, default=False)

    def load(self, width: int, height: int, color: Union[rgb, rgba]) -> None:
        if not self.loaded:
            font_size = getFontDimensions(self.text, self.style, width, height)
            font = pg.font.Font(pg.font.match_font(self.style), font_size) if self.style else pg.font.Font(None, font_size)
            object.__setattr__(self, 'text_surface', font.render(self.text, False, color.get()))
            object.__setattr__(self, 'loaded', True)

    def set_alpha(self, alpha: int = 255) -> None:
        self.text_surface.set_alpha(alpha)

    def rotate(self, rotation: int = 0) -> None:
        #print(self.text_surface)
        object.__setattr__(self, 'text_surface', pg.transform.rotate(self.text_surface, -rotation))

    def size(self) -> Tuple[int, int]:
        return self.text_surface.get_size()

    def get(self, width: int, height: int) -> pg.Surface:
        return pg.transform.scale(self.text_surface, (width, height))
    
class Button:
    def __init__(self, width: int, height: int, pos: vec2, label: Union[None, str], runOnClick: Callable) -> None:
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

    def onClick(self, pos: vec2) -> None:
        if self.range.collidepoint(*pos.get()):
            self.runOnClick()

    def draw(self, window: 'Window', design: int = 0, fontStyle: Union[str, None] = None, fontColor: rgb = rgb(0, 0, 0), outlined: bool = False, outline_depth: int = 0, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), outlineColor: Union[rgb, rgba] = rgba(255, 255, 255, 255), border_radius: int = 20, texture: Union[None, Texture] = None, outlineTexture: Union[None, Texture] = None, scaled: bool = True, scaledOutline: bool = True, transparency: int = 255, transparencyOutline: int = 255, rotation: int = 0) -> None:
        self.isDrawn = True
        if design == 0:
            window.drawRect(self.pos, self.width, self.height, color, texture, scaled=scaled, transparency=transparency, rotation=rotation)
            if outlined:
                window.drawRect(self.pos, self.width, self.height, outlineColor, outlineTexture, scaled=scaledOutline, transparency=transparencyOutline, rotation=rotation, lineDepth=outline_depth)
        elif design == 1:
            window.drawRect(self.pos, self.width, self.height, color, texture, scaled=scaled, transparency=transparency, rotation=rotation, border_radius=border_radius)
            if outlined:
                window.drawRect(self.pos, self.width, self.height, outlineColor, outlineTexture, scaled=scaledOutline, transparency=transparencyOutline, rotation=rotation, border_radius=border_radius, lineDepth=outline_depth)
        if self.label != None:
            window.drawText(self.pos, self.width, self.height - ((self.height // 2) // 4), self.label, fontColor, fontStyle, rotation=rotation, transparency=transparency)

    def drawHitbox(self, screen: pg.Surface, color: Union[rgb, rgba] = rgba(150, 0 ,0, 255)) -> None:
        pg.draw.rect(screen, color.get(), (self.x, self.y, self.width, self.height), 1)

initialized_texts: List[Text] = []
initialized_textures: List[Texture] = []

class Surface:
    def __init__(self, width: int, height: int) -> None:
        self.surf: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        self.ClearColor: Union[rgb, rgba] = rgba(0, 0, 0, 0)

    def setClearColor(self, color: Union[rgb, rgba]) -> None:
        self.ClearColor = color

    def clear(self):
        self.surf.fill(self.ClearColor.get())

    def set_colorkey(self, colorkey: Union[rgb, rgba]) -> None:
        self.surf.set_colorkey(colorkey.get())

    def set_alpha(self, alpha: int) -> None:
        self.surf.set_alpha(alpha)

    def drawLine(self, pos1: vec2, pos2: vec2, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), depth: int = 1) -> None:
        pg.draw.line(self.surf, color.get(), pos1.get(), pos2.get(), depth)

    def drawRect(self, pos: vec2, width: int, height: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texturePath: Union[None, str] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255, border_radius: int = 0) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.rect(mask, color.get(), (0, 0, width, height), lineDepth, border_radius)
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
            texture.convert(width, height)
            texture.rotate(rotation)
            texture.apply(self.surf, mask, topleft, transparency)
            texture.reset()
        else:
            self.surf.blit(mask, topleft.get())

    def drawCircle(self, pos: vec2, radius: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texturePath: Union[None, str] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(radius * 2, radius * 2, "tl")
        mask: pg.Surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(mask, color.get(), (radius, radius), radius, lineDepth)
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
            texture.convert(radius*2, radius*2)
            texture.rotate(rotation)
            texture.apply(self.surf, mask, topleft, transparency)
            texture.reset()
        else:
            self.surf.blit(mask, topleft.get())

    def drawTriangle(self, pos: vec2, width: int, height: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texturePath: Union[None, str] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.polygon(mask, color.get(), [((width//2) - 2, 0), (0, height - 2), (width - 2, height - 2)], lineDepth)
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
            texture.convert(width, height)
            texture.rotate(rotation)
            texture.apply(self.screen, mask, topleft, transparency)
            texture.reset()
        else:
            self.surf.blit(mask, topleft.get())

    def drawText(self, pos: vec2, width: int, height: int, text: str, color: Union[rgb, rgba] = rgba(0, 0, 0, 255), fontStyle: Union[None, str] = None, *, rotation: int = 0, transparency: int = 255) -> None:
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
        self.surf.blit(text_instance.get(width - ((width // 2) // 4), height - ((height // 2) // 4)), vec2(topleft.x + ((width // 2) // 4) // 2, topleft.y + ((height // 2) // 4) // 2).get())
        
    def get(self) -> pg.Surface:
        return self.surf

class Window:
    def __init__(self, width: int, height: int, caption: str, caption_icon: str = "none", window_flags: int = 0) -> None:
        self.screen: pg.Surface = pg.display.set_mode((width, height), window_flags)
        pg.display.set_caption(caption)
        if caption_icon != "none":
            pg.display.set_icon(pg.image.load(caption_icon))

        self.clock = pg.time.Clock()
        self.running: bool = False

        self.ClearColor: rgb = rgb(0, 0, 0)
        
        self.hitboxColor: Union[rgb, rgba] = rgb(0,0,0)
        self.drawHitboxes: bool = False

        self.visual_buttons: List[Button] = []

        self.keys_down: Dict[str, bool] = { key_name: False for key_name in keys.values() }
        self.just_pressed_keys: List[str] = []
        self.just_released_keys: List[str] = []

        self.Mouse_Moved: bool = False
        self.ScrollSpeed: int = 0
        self.ScrollDIR: Dict[str, bool] = ScrollDIR.copy()

        self.buttons_down: Dict[str, bool] = { button_name: False for button_name in mouse_buttons.values() }
        self.just_pressed_buttons: List[str] = []
        self.just_released_buttons: List[str] = []

        self.escape_sequence: Union[Tuple[str, ...], str] = "ESCAPE"
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

    def drawLine(self, pos1: vec2, pos2: vec2, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), depth: int = 1) -> None:
        pg.draw.line(self.screen, color.get(), pos1.get(), pos2.get(), depth)

    def drawRect(self, pos: vec2, width: int, height: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texturePath: Union[None, str] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255, border_radius: int = 0) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.rect(mask, color.get(), (0, 0, width, height), lineDepth, border_radius)
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
            texture.convert(width, height)
            texture.rotate(rotation)
            texture.apply(self.screen, mask, topleft, transparency)
            texture.reset()
        else:
            self.screen.blit(mask, topleft.get())

    def drawCircle(self, pos: vec2, radius: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texturePath: Union[None, str] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(radius * 2, radius * 2, "tl")
        mask: pg.Surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(mask, color.get(), (radius, radius), radius, lineDepth)
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
            texture.convert(radius*2, radius*2)
            texture.rotate(rotation)
            texture.apply(self.screen, mask, topleft, transparency)
            texture.reset()
        else:
            self.screen.blit(mask, topleft.get())

    def drawTriangle(self, pos: vec2, width: int, height: int, color: Union[rgb, rgba] = rgba(255, 255, 255, 255), texturePath: Union[None, str] = None, *, scaled: bool = True, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(width, height, "tl")
        mask: pg.Surface = pg.Surface((width, height), pg.SRCALPHA)
        pg.draw.polygon(mask, color.get(), [((width//2) - 2, 0), (0, height - 2), (width - 2, height - 2)], lineDepth)
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
            texture.convert(width, height)
            texture.rotate(rotation)
            texture.apply(self.screen, mask, topleft, transparency)
            texture.reset()
        else:
            self.screen.blit(mask, topleft.get())

    def drawText(self, pos: vec2, width: int, height: int, text: str, color: Union[rgb, rgba] = rgba(0, 0, 0, 255), fontStyle: Union[None, str] = None, *, rotation: int = 0, transparency: int = 255) -> None:
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
        self.screen.blit(text_instance.get(width - ((width // 2) // 4), height - ((height // 2) // 4)), vec2(topleft.x + ((width // 2) // 4) // 2, topleft.y + ((height // 2) // 4) // 2).get())

    def drawSurface(self, topleft: vec2, surface: Surface) -> None:
        self.screen.blit(surface.get(), topleft.get())

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

    def getMousePos(self) -> vec2:
        return vec2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

    def getScrollSpeed(self) -> int:
        return self.ScrollSpeed

    def hasMouseMoved(self) -> bool:
        return self.Mouse_Moved

    def addButton(self, button: Button) -> None :
        self.visual_buttons.append(button)

    def setClearColor(self, color: Union[rgb, rgba]) -> None:
        self.ClearColor = color

    def get_width(self) -> int:
        return self.screen.get_width()
    
    def get_height(self) -> int:
        return self.screen.get_height()
    
    def getSize(self) -> Tuple[int, int]:
        return self.screen.get_width(), self.screen.get_height()

    def clear(self) -> None:
        self.screen.fill(self.ClearColor.get())

    def startGameLoop(self, gameLoop: Callable, escape_sequence: Union[Tuple[str, ...], str], framerate: int) -> None:
        self.escape_sequence = escape_sequence
        self.framerate = framerate

        self.running = True

        while self.running:

            self.current = pg.time.get_ticks()
            self.last_time = self.current

            self.just_pressed_keys.clear()
            self.just_pressed_buttons.clear()
            self.just_released_keys.clear()
            self.just_released_buttons.clear()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key in keys:
                        self.keys_down[keys[event.key]] = True
                        self.just_pressed_keys.append(keys[event.key])
                    escape = False
                    if isinstance(escape_sequence, str):
                        escape = self.isKeyPressed(escape_sequence)     
                    else:
                        escape = all(self.isKeyPressed(key) for key in escape_sequence)    
                    if escape:
                        self.running = False
                elif event.type == pg.KEYUP:
                    if event.key in keys:
                        self.keys_down[keys[event.key]] = False
                        self.just_released_keys.append(keys[event.key])
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button in mouse_buttons:
                        self.buttons_down[mouse_buttons[event.button]] = True
                        self.just_pressed_buttons.append(mouse_buttons[event.button])
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button in mouse_buttons:
                        self.buttons_down[mouse_buttons[event.button]] = False
                        self.just_released_buttons.append(mouse_buttons[event.button])
                if event.type == pg.MOUSEWHEEL:
                    self.ScrollSpeed = event.y
                    if event.y > 0:
                        self.ScrollDIR["UP"] = True
                        self.ScrollDIR["DOWN"] = False
                    elif event.y < 0: 
                        self.ScrollDIR["UP"] = False
                        self.ScrollDIR["DOWN"] = True
                else:
                    self.ScrollSpeed = 0
                if event.type == pg.MOUSEMOTION:
                    self.Mouse_Moved = True
                else:
                    self.Mouse_Moved = False

            if self.ScrollSpeed == 0:
                self.ScrollDIR["UP"] = False
                self.ScrollDIR["DOWN"] = False

            if not self.running:
                break     

            for button in self.visual_buttons:
                button.isDrawn = False       
            
            gameLoop()

            if self.drawHitboxes:
                for button in self.visual_buttons:
                    if button.isDrawn:
                        button.drawHitbox(self.screen, self.hitboxColor)

            if self.wasButtonPressed("LEFT"):
                for button in self.visual_buttons:
                    if button.isDrawn:
                        button.onClick(self.getMousePos())

            if self.getTimeDiff() >= 1:
                self.fps = self.clock.get_fps()
                self.last_update = self.current

            pg.display.update()
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