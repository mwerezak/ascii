
import time
import console
import keyboard
from layouts import VerticalFlow
from decorators import Anchor
from textwidgets import Label


class Menu (object):
    def __init__ (self):
        self._items = []
        self._idx = None
        self._layout = VerticalFlow()
    
    def _update_layout (self):
        self._layout.items = [item.get_widget(i == self._idx) for i, item in enumerate(self._items)]
    
    @property
    def selected_item (self):
        if self._idx is None:
            return None
        return self._items[self._idx]
    
    @selected_item.setter
    def selected_item (self, value):
        self._idx = self._items.index(value)
        self._update_layout()
        
    def add_item (self, item):
        self._items.append(item)
        self._update_layout()
        
    def select_next (self):
        if self._idx is None:
            self._idx = 0
        else:
            self._idx += 1
        
        if self._idx >= len(self._items):
            self._idx = None
        
        self._update_layout()
            
    def select_prev (self):
        if self._idx is None:
            self._idx = len(self._items) - 1
        else:
            self._idx -= 1
        
        if self._idx < 0:
            self._idx = None
        
        self._update_layout()
        
    def activate (self):
        if self._idx is not None:
            self._items[self._idx].activate()
        
    def width (self): return self._layout.width()
    
    def height (self): return self._layout.height()
        
    def render (self, canvas, x, y):
        self._layout.render(canvas, x, y)
    
class MenuItem (object):
    def __init__(self, text, default_style, selected_style, callback):
        self.callback = callback
        self._default_widget = Label(text, **default_style)
        self._selected_widget = Label(text, **selected_style)
    
    def get_widget (self, selected):
        if selected:
            return self._selected_widget
        else:
            return self._default_widget
    
    def activate (self):
        self.callback()

class PaintPanel (object):
    pass
    
class ControlLoop (object):
    def __init__(self, foreground=None):
        self.foreground = foreground or console.canvas()
        self._stop = False
        self.handle_input = lambda keyinput: None
        self.render = lambda foreground:None
    
    def stop (self):
        self._stop = True

    def run (self, background):
        while not self._stop and not console.closed():
            self.handle_input(keyboard.get_input())
            
            background.blit_to(self.foreground, 0, 0)
            self.render(self.foreground)
            
            console.flush()
            time.sleep(0.015)

if __name__ == "__main__":
    from canvas import CanvasStyle, Canvas
    import sys
    import colour
    
    item_style = CanvasStyle(fg_colour=colour.white,bg_colour=colour.dark_red)
    selected_style = CanvasStyle(fg_colour=colour.dark_red,bg_colour=colour.white)
    
    file_menu = Menu()
    file_menu.add_item( MenuItem("Foo", item_style, selected_style, lambda: console.set_title("Foo")) )
    file_menu.add_item( MenuItem("Bar", item_style, selected_style, lambda: console.set_title("Bar")) )
    file_menu.add_item( MenuItem("Quit", item_style, selected_style, lambda: sys.exit()) )
    
    def handle_input (key):
        if key.released:
            if key == "up":
                file_menu.select_prev()
            elif key == "down":
                file_menu.select_next()
            elif key == "enter":
                file_menu.activate()
            elif key == "esc":
                sys.exit()
    
    def render (canvas):
        file_menu.render(canvas, 0, 0)
    
    console.init(40,20, "Menu Test")
    
    bg = Canvas(40,20)
    
    loop = ControlLoop()
    loop.handle_input = handle_input
    loop.render = render
    loop.run(bg)