from pynput import keyboard
import threading
from pynput.keyboard import Key

_enter_pressed_flag = threading.Event()
_listener = None

ENTER_KEYS = {
    Key.enter,
    Key.space,
    Key.cmd
}

def set_enter_key_listener():
    global _listener
    
    def on_press(key):
        if key in ENTER_KEYS:
            _enter_pressed_flag.set()
    
    _enter_pressed_flag.clear()
    
    if _listener:
        _listener.stop()
    
    _listener = keyboard.Listener(on_press=on_press)
    _listener.start()
    return _listener

def is_enter_pressed():
    return _enter_pressed_flag.is_set()

def clear_enter_pressed():
    _enter_pressed_flag.clear()

def cleanup():
    global _listener
    if _listener:
        _listener.stop()
        _listener = None
    _enter_pressed_flag.set()