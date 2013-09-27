import array

class Rectangle (object):
    def __init__ (self,x,y,w,h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
    
    def __copy__(self):
        return Rectangle(self.x, self.y, self.width, self.height)
    
    def __repr__ (self):
        return "<%s.Rectangle object: x=%d, y=%d, width=%d, height=%d>"%(
            self.__module__,self.x,self.y,self.width,self.height)
            
    def contains (self, x, y):
        """Returns True if the given point is inside the rectangle (including edges)."""
        return (x >= self.x and x <= self.x + self.width - 1) and (y >= self.y and y <= self.y + self.height - 1) 
    
    def on_edge (self, x, y):
        on_x = (x >= self.x and x <= self.x + self.width - 1) and (y == self.y or y == self.y + self.height - 1)
        on_y = (x == self.x or x == self.x + self.width - 1) and (y >= self.y and y <= self.y + self.height - 1) 
        return on_x or on_y
        
    def overlaps (self, rect):
        """Returns True if the given Rectangle overlaps this one (including edges)."""
        x1, x2 = self.x, self.x + self.width - 1
        ox1, ox2 = rect.x, rect.x + rect.width - 1
        y1, y2 = self.y, self.y + self.height - 1
        oy1, oy2 = rect.y, rect.y + rect.height - 1 
        
        div_x = (ox1 < x1 and ox2 < x1) or (ox1 > x2 and ox2 > x2)
        div_y = (oy1 < y1 and oy2 < y1) or (oy1 > y2 and oy2 > y2)
        return not div_x and not div_y
    
        
class OrthoLine (object):
    """ Represents a line that may be either horizontal or vertical."""
    HLINE = "hline"
    VLINE = "vline"

    def __init__(self, type, x, y, length):
        self.type = type
        self.x = x
        self.y = y
        self.length = length
    
    def endpoint(self):
        if self.type == HLINE:
            return (x + length - 1, y)
        if self.type == VLINE:
            return (x, y + length - 1)
        raise ValueError("unknown line type: %s"%self.type)