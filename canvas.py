import libtcodpy as dlib
from misc import Rectangle
from colour import Colour

#TODO - wrap LibTCOD background effect flags

## todo: key colour
class Canvas (object):
    """ 
    A canvas for drawing stuff on that can be blitted to a console.
    Provides a wrapper around libTCOD drawing functionality
    """
    
    def __init__(self, w, h, handle=None):
        if handle:
            self._intern = handle
        else:
            self._intern = dlib.console_new(w,h)
        self.x_offset = 0
        self.y_offset = 0
    
    @property
    def width(self):
        return dlib.console_get_width(self._intern)

    @property
    def height(self):
        return dlib.console_get_height(self._intern)
    
    def resize(self, w,h):
        """Changes the size of the canvas, copying over the contents of this canvas.
        Content outside of the new canvas bounds is clipped.
        """
        new = dlib.console_new(w,h)
        bw = min(w, self.width)
        bh = min(h, self.height)
        dlib.console_blit(self._intern, 0, 0, bw, bh, new, 0, 0)    #copy contents
        dlib.console_delete(self._intern)   #dispose old console
        self._intern = new
    
    def __del__(self):
        dlib.console_delete(self._intern)
               
    ## style properties
    @property
    def bg_colour(self):
        return Colour(0,0,0,struct=dlib.console_get_default_background(self._intern))
    
    @bg_colour.setter
    def bg_colour(self, bg):
        if bg is None:
            self.bg_effect = dlib.BKGND_NONE
        else:
            if self.bg_effect == dlib.BKGND_NONE:
                self.bg_effect = dlib.BKGND_SET
            dlib.console_set_default_background(self._intern, bg.get_struct())
        
    @property
    def fg_colour(self):
        """ The default foreground colour which is used for functions that do not explicitly ask for one.
        """
        return Colour(0,0,0,struct=dlib.console_get_default_foreground(self._intern))
    
    @fg_colour.setter
    def fg_colour(self, fg):
        dlib.console_set_default_foreground(self._intern, fg.get_struct())
       
    @property
    def bg_effect(self):
        """ The default background colour which is used for functions that do not explicitly ask for one.
        """
        return dlib.console_get_background_flag(self._intern)
       
    @bg_effect.setter
    def bg_effect(self, effect):
        """ The default background effect which is used for functions that do not explicitly ask for one.
        """
        return dlib.console_set_background_flag(self._intern, effect)
        
    ## drawing functions
    def clear(self):
        dlib.console_clear(self._intern)
    
    def blit_to(self, target, x, y, rect=None, bg_alpha=1.0, fg_alpha=1.0):
        """Blits a rectangular area of a canvas onto another canvas.
        The upper right corner of rectangular area is positioned on the
        target Canvas at x,y. If rect is specified, only that area will
        be blitted. Otherwise, the entire area of the Canvas is used
        """
        if not rect: rect = Rectangle(0,0,0,0)
        dlib.console_blit(self._intern, rect.x, rect.y, rect.width, rect.height, target._intern, x, y, fg_alpha, bg_alpha)
               
    def fill_rect(self, rect, opaque=True, effect=dlib.BKGND_DEFAULT):
        dlib.console_rect(self._intern, rect.x + self.x_offset, rect.y + self.y_offset, 
                          rect.width, rect.height, opaque, effect)
    
    def put_char(self, x, y, ch):
        """ Puts the specified character or tile at the x, y coordinate, offset by this Canvas' offset values.
            ch can be either a string or integral type.
        """
        x += self.x_offset
        y += self.y_offset
        dlib.console_put_char(self._intern, x, y, ch)
        
    def hline(self, x, y, len, ch):
        for i in range(0, len):
            self.put_char(x+i,y,ch)
            
    def vline(self, x, y, len, ch):
        for i in range(0, len):
            self.put_char(x,y+i,ch)
            
    def set_cell(self, x, y, ch=None, bg=None, fg=None, bg_effect=dlib.BKGND_DEFAULT):
        x += self.x_offset
        y += self.y_offset
        if bg: dlib.console_set_char_background(self._intern, x, y, bg.get_struct(), bg_effect)
        if fg: dlib.console_set_char_background(self._intern, x, y, fg.get_struct())
        if ch: dlib.console_put_char(self._intern, x, y, ch)
                   
    ## text functions
    def printstr(self, x, y, s):
        x += self.x_offset
        y += self.y_offset
        dlib.console_print(self._intern, x, y, s)
        
    ## misc
    def get_char(self, x, y):
        x += self.x_offset
        y += self.y_offset
        return chr(dlib.console_get_char(self._intern,x,y)) #TODO return a Tile object instead


class CanvasState (object):
    """ Allows you to use the Canvas's properties such as bg_colour, fg_colour, text_align, 
        and automatically restores them once you are done.
    """
    
    def __init__(self, canvas, x_offset=0, y_offset=0, canvas_style=None):
        self.canvas = canvas
        self.style = canvas_style
        self.x = x_offset
        self.y = y_offset
       
    def _save_state(self, canvas):    
        self.bg_colour = canvas.bg_colour
        self.fg_colour = canvas.fg_colour
        self.bg_effect = canvas.bg_effect
        #self.text_align = canvas.text_align
        self.x_offset = canvas.x_offset
        self.y_offset = canvas.y_offset
    
    def _restore_state(self, canvas):
        canvas.bg_colour = self.bg_colour
        canvas.fg_colour = self.fg_colour
        canvas.bg_effect = self.bg_effect
        #canvas.text_align = self.text_align
        canvas.x_offset = self.x_offset
        canvas.y_offset = self.y_offset
        
    def __enter__(self):
        self._save_state(self.canvas)
        self.canvas.x_offset += self.x
        self.canvas.y_offset += self.y
        if self.style:
            self.style.apply(self.canvas)
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self._restore_state(self.canvas)
        return False
        
class CanvasStyle (dict):
    """ A container used to hold style properties of a ui object, such as a widget.
    """
    def __init__(self, **style_mapping):
        for prop, val in style_mapping.iteritems():
            self[prop] = val
    
    def apply(self, canvas):
        """Applies this Widget's style properties to a canvas."""
        for prop, val in self.iteritems():
            setattr(canvas, prop, val)