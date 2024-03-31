import pygame as pg
from dataclasses import dataclass
from typing import Dict, List, Tuple
from math import sqrt
from collections.abc import Callable
import threading
import time

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
