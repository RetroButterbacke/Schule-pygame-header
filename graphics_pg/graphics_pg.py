from collections.abc import Callable
from .utils import *
from typing import List, Tuple, Dict
from functools import reduce
from dataclasses import dataclass, field
import pygame as pg
import time
import threading
from math import sqrt
import sys

__all__ = ["Button", "Surface", "Window", "init", "quit"]

@dataclass(frozen=True, eq=True)
class Texture:
    filePath: str
    texture: pg.Surface = field(compare=False, init=False)
    original: pg.Surface = field(compare=False, init=False)

    def load(self) -> bool:
        try:
            object.__setattr__(self, 'original', pg.image.load(self.filePath))
            object.__setattr__(self, 'texture', self.original)
            return True
        except pg.error as e:
            print(f"Error loading texture: {e}")
            return False 
            
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
           
        if start.x > self.texture.get_width() - 1 or start.x < 0 or start.y > self.texture.get_height() - 1 or start.y < 0:
            raise IndexError("Start pos is out of range")
        
        result = pg.Surface((width, height), pg.SRCALPHA)
        
        for x in range(0, width):
            for y in range(0, height):
                result.set_at((x, y), self.texture.get_at((start.x + x, start.y + y)))
                #sys.exit()
                
        object.__setattr__(self, 'texture', result)
            
    def reset(self) -> None:
        object.__setattr__(self, 'texture', self.original)

    def convert(self, width: int, height: int, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None) -> None:
        if scaled:
            if starting_point and part_width and part_height:
                self.__load_texturePart__(starting_point, part_width, part_height)
                object.__setattr__(self, 'texture', pg.transform.scale(self.texture, (width, height)))
            else:
                object.__setattr__(self, 'texture', self.getScaled(width, height))
        else:
            if not starting_point:
                self.__load_tileTexture__(width, height)
            else:
                self.__load_texturePart__(starting_point, width, height)
        

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

        tl = True
        
        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                tl = texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            if tl:
                texture.convert(width, height, scaled, starting_point, part_width, part_height)
                texture.rotate(rotation)
                if colorkey:
                    texture.set_colorkey(colorkey)
                texture.apply(self.surf, mask, topleft, transparency)
                texture.reset()
            else:
               self.screen.blit(mask, topleft._get()) 
        else:
            self.surf.blit(mask, topleft._get())

    def drawCircle(self, pos: vec2, radius: int, color: rgb | rgba = rgba(255, 255, 255, 255), texturePath: None | str = None, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(radius * 2, radius * 2, "tl")
        mask: pg.Surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(mask, color._get(), (radius, radius), radius, lineDepth)
        mask.set_alpha(transparency)

        mask = pg.transform.rotate(mask, -rotation)

        tl = True
        
        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                tl = texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            if tl:
                texture.convert(width, height, scaled, starting_point, part_width, part_height)
                texture.rotate(rotation)
                if colorkey:
                    texture.set_colorkey(colorkey)
                texture.apply(self.surf, mask, topleft, transparency)
                texture.reset()
            else:
               self.screen.blit(mask, topleft._get()) 
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

        tl = True
        
        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                tl = texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            if tl:
                texture.convert(width, height, scaled, starting_point, part_width, part_height)
                texture.rotate(rotation)
                if colorkey:
                    texture.set_colorkey(colorkey)
                texture.apply(self.screen, mask, topleft, transparency)
                texture.reset()
            else:
               self.screen.blit(mask, topleft._get()) 
        else:
            self.screen.blit(mask, topleft._get())

    def drawCircle(self, pos: vec2, radius: int, color: rgb | rgba = rgba(255, 255, 255, 255), texturePath: None | str = None, *, scaled: bool = True, starting_point: vec2 | None = None, part_width: int = None, part_height: int = None, colorkey: rgb | None = None, lineDepth: int = 0, rotation: int = 0, transparency: int = 255) -> None:
        global initialized_textures
        topleft: vec2 = pos.convert(radius * 2, radius * 2, "tl")
        mask: pg.Surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(mask, color._get(), (radius, radius), radius, lineDepth)
        mask.set_alpha(transparency)

        mask = pg.transform.rotate(mask, -rotation)

        tl = True
        
        if texturePath != None:
            texture = Texture(texturePath)
            if not texture in initialized_textures:
                tl = texture.load()
                initialized_textures.append(texture)
            else:
                filtered = list(filter(lambda x: x == texture, initialized_textures))
                texture = filtered[-1]
            if tl:
                texture.convert(width, height, scaled, starting_point, part_width, part_height)
                texture.rotate(rotation)
                if colorkey:
                    texture.set_colorkey(colorkey)
                texture.apply(self.screen, mask, topleft, transparency)
                texture.reset()
            else:
               self.screen.blit(mask, topleft._get()) 
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
                # Clearing the text list so that it does not take to much memory
                ## it's only there so that text does not get initialized every frame
                ## so it can be cleared every miniute
                if self.clear_update == 0:
                    initialized_texts.clear()
                    self.clear_update = 60
                elif self.clear_update > 0:
                    self.clear_update -= 1

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
