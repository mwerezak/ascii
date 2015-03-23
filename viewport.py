import libtcodpy as dlib
import console
from canvas import Canvas, CanvasState
from events import EventSource
from misc import Rectangle
from decorators import *
from textwidgets import *
from shapes import *


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

