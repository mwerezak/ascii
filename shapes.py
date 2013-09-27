from canvas import CanvasState, CanvasStyle
import libtcodpy as dlib

class RectangleShape(object):
    def __init__(self, width, height, char=None, **style):
        self.style = CanvasStyle(style)
        self._w = width
        self._h = height
        self.char = char
        
    def width (self): return self._w
    def set_width (self, w): self._w = w   
    def height (self): return self._h
    def set_height (self, h): self._h = h
    
    def render(self, canvas, x, y):
        with CanvasState(canvas,x,y):
            self.style.apply(canvas)
            for i in range(self._w):
                for j in range (self._h):
                    canvas.put_char(i,j,self.char)


#OvalShape

class Cell(object):
    def __init__(self, char, **style):
        self.style = CanvasStyle(style)
        self.char = char
        
    def width (self): return 1
    def height (self): return 1
    
    def render(self,canvas,x,y):
        with CanvasState(canvas,x,y):
            self.style.apply(canvas)
            canvas.put_char(0,0,self.char)
                

class CellArray(object):
    def __init__(self, width, height, content, bg_char=" ", **style):
        """ Content must be a sequence of single characters or None values of length equal to width * height.
            For each item that is None the corresponding cell will not be rendered.
            bg_char specifies the characters that will be ignored. This parameter may be None
        """
        self.style = CanvasStyle(style)
        self._w = width
        self._h = height
        self.bg_char = bg_char
               
        self.content = []
        for item in content:
            if len(item) == 1:
                self.content.append(item)
            else:
                self.content.extend(item)
                
        if len(self.content) != width * height:
            raise ValueError("length of given content does not match the size of the CellArray")
        
    def width (self): return self._w
    def height (self): return self._h
    
    def render(self, canvas, x, y):
        width = self.width()
        with CanvasState(canvas, x, y):
            self.style.apply(canvas)
            for i in range(self._w):
                for j in range (self._h):
                    idx = i + j*width
                    char = self.content[idx]
                    if char is not None and char != self.bg_char:
                        canvas.put_char(i,j,char)