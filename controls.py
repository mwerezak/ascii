import libtcodpy as dlib
import console
from canvas import Canvas, CanvasState
from layouts import VerticalLayout
from events import EventSource
from misc import Rectangle
from decorators import *
from textwidgets import *
from shapes import *

class ControlBase (object):
    """ Runs a get input/update display loop.
    """
    
    def __init__ (self):
        """ bg_canvas is a canvas containing the background for the widget. The contents of this canvas are
            unchanged. fg_canvas is the canvas on which the Control will be drawn.
        """
        self.enabled = True
        self.children = []
    
    def add_child (self, control):
        self.children.append(control)
    
    def remove_child(self, control):
        self.children.remove(control)
        
    def handle_keyinput(self, input):
        """ Override in subclass. """
        pass
        
    def render (self, canvas, x, y):
        """ Override in subclass. """
        pass
    
    def run (self, bg_canvas, fg_canvas=None):
        canvas = fg_canvas or Canvas(bg_canvas.width, bg_canvas.height)
        #TODO: implement


def ControlLoop (object):
    def __init__ (self, root_control, background, foreground):
        self.root_control = root_control
        self.background = background
        self.foreground = foreground
    
        
    
    
        
#TODO
#TextInput
#Menu
#Tabs        #view components on different tabs


class Viewport (object):
    """Allows for a scrollable view of a larger Canvas."""
    def __init__(self, canvas, view_width, view_height):
        self.canvas = canvas
        self.viewport = Rectangle(0,0,view_width,view_height)
    
    def to_screen_coord(self, x, y):
        """Converts canvas coordinates to screen coordinates."""
        return (x - self.viewport.x, y - self.viewport.y)
    
    def to_parent_coord(self, x, y):
        """Converts screen coordinates to parent canvas coordinates."""
        return (x + self.viewport.x, y + self.viewport.y)
           
    def on_screen(self, x, y):
        """Returns True if the parent coords x,y are inside the viewport."""
        return self.viewport.contains(x,y)
    
    def _limit_x(self, x):
        ## returns x so that it is a valid x-coordinate of the viewport
        if x + self.viewport.width > self.canvas.width: 
            x = self.canvas.width - self.viewport.width
        if x < 0: x = 0
        return x
    
    def _limit_y(self, y):
        ## returns x so that it is a valid x-coordinate of the viewport
        if y + self.viewport.height > self.canvas.height: 
            y = self.canvas.height - self.viewport.height
        if y < 0: y = 0
        return y
        
    def width(self): return self.viewport.width
    
    def height(self): return self.viewport.height
    
    def render(self, canvas, x, y):
        self.canvas.blit_to(canvas, x, y, self.viewport)
        
    def scroll_up(self):
        if self.viewport.y > 0: 
            self.viewport.y -= 1
    
    def scroll_down(self):
        if self.viewport.y + self.viewport.height < self.canvas.height: 
            self.viewport.y += 1
            
    def scroll_left(self):
        if self.viewport.x > 0: 
            self.viewport.x -= 1
    
    def scroll_right(self):
        if self.viewport.x + self.viewport.width < self.canvas.width: 
            self.viewport.x += 1
    
    def set_viewport(self,x,y):
        self.viewport.x = self._limit_x(x)
        self.viewport.y = self._limit_y(y)
    
    def center_on(self, x, y):
        """Centers the viewport on the given parent coords."""
        self.viewport.x = self._limit_x(x - self.viewport.width/2)
        self.viewport.y = self._limit_y(y - self.viewport.height/2)



class ButtonControl (object): pass
        
class SampleListControl (object):
    def __init__ (self, items, min_width, halign="left"):
        self._items = items
        self.selected = []
        self.cursor = None
        
        self.min_width = min_width
        self.halign = halign
        
        self._layout = VerticalLayout()
        self._update_layout()
        
    def get_cursor_item(self):
        if self.cursor is not None:
            return self._items[self.cursor]
        return None
    
    def activate(self):
        if self.cursor is not None:
            item = self.get_cursor_item()
            if item not in self.selected:
                self.selected.append(item)
            else:
                self.selected.remove(item)
    
    def scroll_up(self):
        if self.cursor is None:
            self.cursor = len(self._items) - 1
        else:
            self.cursor -= 1
            if self.cursor < 0:
                self.cursor = None
    
    def scroll_down(self):
        if self.cursor is None:
            self.cursor = 0
        else:
            self.cursor += 1
            if self.cursor >= len(self._items):
                self.cursor = None
           
    def _update_layout (self): 
        self._layout.clear()
        for item in self._items:
            label = Label(item)
            if item in self.selected:
                label.style["fg_colour"] = dlib.yellow
                if self.halign == "center":
                    label.text = "> " + item + " <"
                else:
                    label.text = "> " + item
            
            label = label >> Anchor(self.halign, "center", self.min_width)
            
            if self.cursor is not None and item == self.get_cursor_item():
                label.style["fg_colour"] = dlib.black
                label = label >> Fill(bg_colour=dlib.green)
            self._layout.add(label)
    
    def width(self): return self._layout.width()
    
    def height(self): return self._layout.height()
    
    def render(self, canvas, x, y):
        self._update_layout()
        self._layout.render(canvas, x, y)

## Test Code
if __name__ == "__main__":
    import console
    import keyinput
    from layouts import *
    from lines import *
    from shapes import *
    from colour import *
    
    console.init(40,40,"Control Test")
    
    items = ["item #%d"%(i+1) for i in range(9)]    
    menu = SampleListControl(items, 11, "center")
       
    bg = RectangleShape(console.width(), console.height(), "#")
       
    panel = AbsoluteLayout()
    panel.add(menu >> Border(double_line, fg_colour=white) >> Padding(1,1) >> Fill(bg_colour=dark_grey) >> Border(single_line, fg_colour=gold) >> Padding(2,2), 0, 0)
        
    def handle_input (key):
        if key.released:
            if key == "space" or key == "enter": menu.activate()
        else:
            if key == "up": menu.scroll_up()
            if key == "down": menu.scroll_down()
               
    while not console.closed():
        handle_input(keyinput.get_input())
        
        bg.render(console.canvas(), 0, 0)
        panel.render(console.canvas(), 0, 0)
        
        console.flush()
        #time.sleep(0.015)