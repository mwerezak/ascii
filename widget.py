import libtcodpy as dlib
from canvas import Canvas, CanvasState, CanvasStyle
from misc import Rectangle

class Widget (object):
    """ A Widget is an object that handles drawing and appearance of UI Controls.
    """
    def __init__(self, **style):
        self.style = CanvasStyle(style)
    
    def width (self):
        """ Override in a subclass."""
        return 0
    
    def height (self): 
        """ Override in a subclass."""
        return 0
       
    def render(self, canvas, x, y):
        """ Override in a subclass. The widget must draw itself with it's upper left corner at x,y. """
        with CanvasState(canvas, x, y):
            self.style.apply(canvas)
        
    
class Align(object):
    """ Repositions a widget so that it's bounding box is aligned relative to the rendering coordinates. 
        Align is not really a widget since violates the rule that a widget is positioned with it's upper left corner at x,y.
        Since naively using it as a widget can cause things to not sometimes draw properly, it exposes a render_aligned() 
        method instead of the usual render().
    """
    def __init__(self, target, halign="left", valign="top"):
        self.target = target
        self.valign = valign
        self.halign = halign
    
    def x_offset(self):
        """Returns the offset between the upper-left corner and the render location x,y."""
        width = self.target.width()
        if self.halign == "right":
            return 1 - width
        if self.halign == "center":
            return -(width/2)
        if self.halign == "left":
            return 0
        raise ValueError("Unrecognized horizontal alignment: %s"%self.halign)
        
    def y_offset(self):
        """Returns the offset between the upper-left corner and the render location x,y."""
        height = self.target.height()
        if self.valign == "bottom":
            return 1 - height
        if self.valign == "center":
            return -(height/2)
        if self.valign == "top":
            return 0
        raise ValueError("Unrecognized vertical alignment: %s"%self.valign)
    
    def width (self): return self.target.width()
    
    def height (self): return self.target.height()
       
    def render_aligned (self, canvas, x, y):
        self.target.render(canvas,x + self.x_offset(),y + self.y_offset())