from canvas import CanvasState
from decorators import Anchor, Padding, Align


class VerticalFlow(object):
    """ Attributes
        items: a list of items to display.
    """
    def __init__(self):
        self.items = []
    
    def width(self):
        return max([item.width() for item in self.items])
    
    def height(self):
        return sum([item.height() for item in self.items])
        
    def render(self, canvas, x, y):
        with CanvasState(canvas, x, y):
            y = 0
            for item in self.items:
                item.render(canvas,0,y)
                y += item.height()
                
                
class HorizontalFlow(object):
    """ Attributes
        items: a list of items to display.
    """
    def __init__(self):
        self.items = []
    
    def width(self):
        return sum([item.width() for item in self.items])
    
    def height(self):
        return max([item.height() for item in self.items])
    
    def render(self, canvas, x, y):
        with CanvasState(canvas, x, y):
            x = 0
            for item in self.items:
                item.render(canvas,x,0)
                x += item.width()

#TODO
class GridFlow(object):
    """ Attributes
        items: a mapping of (row, col) tuples to items.
    """
    def __init__ (self):
        self.items = {}
    
    def shape (self):
        """ Returns a tuple (num_rows, num_cols) indicating the number of rows and
            columns of this grid. 
        """
        row_indices, col_indices = zip(*self.items.iteritems())
        return ( max(row_indices+1), max(col_indices+1) )
        
    def num_rows (self): return self.shape()[0]
    
    def num_cols (self): return self.shape()[1]
    
    
    def width(self): raise NotImplementedError()
    def height(self): raise NotImplementedError()
    def render(self, canvas, x, y): raise NotImplementedError()