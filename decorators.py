#Border

import libtcodpy as dlib
from widget import Align
from canvas import CanvasState, CanvasStyle
from lines import LinePainter
from misc import Rectangle

class UnboundDecoratorError (Exception): pass

class Decorator(object):
    """ A decorator is a widget that wraps another widget to modify its appearance in some way.
        For example, a Decorator could add a border or background fill, align the widget with a
        coord or anchor it within a rectangular area.
    """    
    def __init__(self, target=None):
        self.target = target
    
    def bind (self, target):
        self.target = target
        
    def __rrshift__(self, target):
        """x >> y wraps x inside the decorator y"""
        self.bind(target)
        return self
        
    def __rshift__(self, other):
        if not hasattr(other, "bind"):
            raise NotImplemented(">> operator is not implemented for types '%s' and '%s'"%(type(self).__name__, type(other).__name__))
        other.bind(self)
        return other
       
    def width (self): return self.target.width()
    
    def height (self): return self.target.height()
    
    def render(self, canvas, x, y):
        if self.target is None:
            raise UnboundDecoratorError("cannot render an unbound decorator.")
        self.target.render(canvas,x,y)


class Fill(Decorator):
    def __init__(self, **style):
        Decorator.__init__(self)
        self.style = CanvasStyle(**style)
        self.target = None
       
    def width (self): return self.target.width()
    
    def height (self): return self.target.height()
    
    def render(self,canvas,x,y):       
        with CanvasState(canvas,x,y):
            self.style.apply(canvas)
            canvas.fill_rect(Rectangle(0,0,self.target.width(), self.target.height()))
        #render the target after so that it appears on top of the fill
        self.target.render(canvas,x,y)  

class Padding(Decorator):
    def __init__(self, hpad=None, vpad=None, left=None, right=None, top=None, bottom=None):
        Decorator.__init__(self)
        self.left = left or hpad or 0
        self.right = right or hpad or 0
        self.top = top or vpad or 0
        self.bottom = bottom or vpad or 0
        
    def width (self): return self.target.width() + self.left + self.right
    
    def height (self): return self.target.height() + self.top + self.bottom
    
    def render (self, canvas, x, y):
        self.target.render(canvas, x + self.left, y + self.top)
            
    def __repr__ (self):
        return "<%s.Padding object: left=%d, right=%d, top=%d, bottom=%d>"%(
            self.__module__,self.left,self.right,self.top,self.bottom)
        
class Anchor(Decorator):
    def __init__(self, halign, valign, min_width=0, min_height=0):
        Decorator.__init__(self)
        self.halign = halign
        self.valign = valign
        self.min_width = min_width
        self.min_height = min_height
        
    def width (self): return max(self.min_width, self.target.width())
    
    def height (self): return max(self.min_height, self.target.height())
        
    def _x_inner (self): 
        if self.halign == "left": 
            return 0
        if self.halign == "center": 
            return self.width()/2
        if self.halign == "right": 
            return self.width() - 1
        raise ValueError("Unrecognized horizontal alignment: %s"%self.halign)
        
    def _y_inner (self):
        if self.valign == "top": 
            return 0
        if self.valign == "center": 
            return self.height()/2
        if self.valign == "bottom": 
            return self.height() - 1
        raise ValueError("Unrecognized vertical alignment: %s"%self.valign)
        
    def render (self,canvas,x,y):
        align = Align(self.target, halign=self.halign, valign=self.valign)
        align.render_aligned(canvas, x + self._x_inner(), y + self._y_inner())
        
    def __repr__(self):
        return "<%s.Anchor object: halign=%s, valign=%s, min_width=%d, min_height=%d>"%(
            self.__module__, self.halign, self.valign, self.min_width, self.min_height)

      
class Border(Decorator):
    def __init__(self, linestyle, left=True, right=True, top=True, bottom=True, **style):
        Decorator.__init__(self)
        self.style = CanvasStyle(**style)
        self.linestyle = linestyle
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        
    def width (self): 
        w = self.target.width()
        if self.left: w += 1
        if self.right: w += 1
        return w
    
    def height (self): 
        h = self.target.height()
        if self.top: h += 1
        if self.bottom: h += 1
        return h
        
    def render (self, canvas, x, y):   
        x_off, y_off = 0,0
        if self.top: y_off += 1
        if self.left: x_off += 1
        
        w = self.width()
        h = self.height()
        
        #draw target
        self.target.render(canvas, x+x_off, y+y_off)
        
        #draw borders
        with CanvasState(canvas,x,y):
            self.style.apply(canvas)
            
            lines = LinePainter(self.linestyle)
            if self.left: lines.add("vline", 0, 0, h)
            if self.right: lines.add("vline", w-1, 0, h)
            if self.top: lines.add("hline", 0, 0, w)
            if self.bottom: lines.add("hline", 0, h-1, w)

            lines.paint(canvas)
            
            
            
            