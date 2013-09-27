"""
Wrapper for the root console in libtcod.
"""

import libtcodpy as dlib
from canvas import Canvas

class ConsoleError(Exception): pass

class _RootCanvas(Canvas):
    """Wrapper for the root console in Lib TCOD"""
    def __init__(self, handle):
        Canvas.__init__(self,0,0,handle)
       
    def __del__ (self): 
        pass


_root = None   #the root canvas
_title = ""
        
def init(w, h, title):
    global _root, _title
    handle = dlib.console_init_root(w, h, title)
    _root = _RootCanvas(handle)
    _title = title
              
def width(): return dlib.console_get_width(None)

def height(): return dlib.console_get_height(None)
    
def title(): return _title

def set_title(title): 
    _title = title
    dlib.console_set_window_title(title)

def fullscreen(): return dlib.console_is_fullscreen()

def set_fullscreen(fullscreen): dlib.console_set_fullscreen(fullscreen)

def closed(): return dlib.console_is_window_closed()

def flush(): dlib.console_flush()

def canvas(): return _root
        
def wait_for_user(): dlib.console_wait_for_keypress(True)