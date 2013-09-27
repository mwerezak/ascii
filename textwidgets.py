from canvas import CanvasState, CanvasStyle
from decorators import Anchor
from misc import Rectangle

class Label(object):
    """A widget that displays a single line of text."""

    def __init__ (self,text, **style):       
        self.style = CanvasStyle(style)
        self.text = text
       
    def width (self): return len(self.text)
    
    def height (self): return 1
               
    def render (self,canvas,x,y):
        with CanvasState(canvas,x,y):
            self.style.apply(canvas)
            canvas.printstr(0,0,self.text)

#TODO: non-breaking space?
class Text(object):
    """ A widget that displays a reflowable column of text. Always starts a new line at newline characters.
    """
    def __init__(self, text, max_width, text_align="left", **style):
        self.style = CanvasStyle(style)
        if max_width <= 0: raise ValueError("max_width must be greater than 0")
        
        self.max_width = max_width
        self.text_align = text_align
        self._lines = []    #A list of Label objects - one for each line
        
        self.text = text
        
    @property
    def text (self):
        return self._text
        
    @text.setter
    def text (self, value):
        self._text = value
        self._lines = [Label(text) for text in self._get_line_text()] #generate lines from text flow
    
    def _split(self, text):
        """ Returns an iterator that breaks text into chunks consisting of a continuous block of non-whitespace followed by a
            continouse block of whitespace.
        """
        if len(text) == 0:
            return
            
        last_ws = False     #was the last character whitespace?
        i = 0               #beginning of chunk index
        for j in range(len(text)):
            if (text[j].isspace() and not last_ws) or text[j] == "\n":
                yield text[i:j]
                i = j       #begin a new chunk
            last_ws = text[j].isspace()
        yield text[i:]
    
    def _get_line_text(self):
        line = ""
        for chunk in self._split(self.text):
            if len(chunk) > 0 and chunk[0] == "\n":         #break on newlines
                yield line
                line = chunk.lstrip()
            elif len(line) + len(chunk) > self.max_width:   #break if the next chunk does not fit
                yield line
                line = chunk.lstrip()
            else:
                line += chunk

            while len(line) > self.max_width:   #break chunks that are larger than max_width
                yield line[:self.max_width]
                line = line[self.max_width:]
        
        if len(line) > 0:
            yield line
        
    def width (self):
        return max([line.width() for line in self._lines])
    
    def height (self):
        return len(self._lines)
    
    def render (self,canvas,x,y):
        anchor = Anchor(halign=self.text_align, valign="top", min_width=self.max_width)
        with CanvasState(canvas,x,y):
            self.style.apply(canvas)
            for i, line in enumerate(self._lines):
                (line >> anchor).render(canvas,0,i)
                
                
## Test Code
if __name__ == "__main__":
    import libtcodpy as dlib
    import console
    from decorators import Border
    from lines import double_line
    
    console.init(30,30,"Text Test")
    
    text = Text('The standard chunk of  \t\n LoremIpsumusedsincethe1500sisreproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also repr\noduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.', 15, bg_colour=dlib.darker_red)
    
    (text >> Border(double_line)).render(console.canvas(), 2, 2)
    console.flush()
    console.wait_for_user()
    