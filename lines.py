
import libtcodpy as dlib
from canvas import CanvasState
from misc import OrthoLine

#TODO implement dashed lines
class LineStyle (object):
    def __init__(self, default, **ch_dict):
        ch_dict[None] = default
        self.char_dict = dict(ch_dict)
        
    def __contains__(self, char):
        return char in self.char_dict.values()
        
    def __getitem__(self, key):
        if key not in self.char_dict:
            return self.char_dict[None]
        return self.char_dict[key]
        
    def __iter__(self):
        return iter(self.char_dict.itervalues())
    
#To create a linestyle of a single character, you only need to use LineStyle('#') for example.
    
single_line = LineStyle(
    dlib.CHAR_CROSS,
    h = dlib.CHAR_HLINE,
    v = dlib.CHAR_VLINE,
    ne = dlib.CHAR_NE,
    nw = dlib.CHAR_NW,
    se = dlib.CHAR_SE,
    sw = dlib.CHAR_SW,
    tw = dlib.CHAR_TEEW,
    te = dlib.CHAR_TEEE,
    tn = dlib.CHAR_TEEN,
    ts = dlib.CHAR_TEES,
    x = dlib.CHAR_CROSS)
                        
double_line = LineStyle(
    dlib.CHAR_DCROSS,
    h = dlib.CHAR_DHLINE,
    v = dlib.CHAR_DVLINE,
    ne = dlib.CHAR_DNE,
    nw = dlib.CHAR_DNW,
    se = dlib.CHAR_DSE,
    sw = dlib.CHAR_DSW,
    tw = dlib.CHAR_DTEEW,
    te = dlib.CHAR_DTEEE,
    tn = dlib.CHAR_DTEEN,
    ts = dlib.CHAR_DTEES,
    x = dlib.CHAR_DCROSS)
   
#linetype enum

class LinePainter(object):
    
    class DrawingLine(OrthoLine):
        def __init__(self,type,x,y,length,style):
            OrthoLine.__init__(self,type,x,y,length)
            self.style = style
    
    def __init__(self, default_linestyle):
        self.default_linestyle = default_linestyle
        self._lines = []
        
    def add(self, type, x, y, length, style=None):
        """ Adds a line of the specified type starting at (x,y) and having a length in cells.
            Lines of type HLINE are drawn to the right from the starting point.
            Lines of type VLINE are drawn down from the starting point.
        """
        if length < 0: raise ValueError("length cannot be negative")
        self._lines.append(self.DrawingLine(type,x,y,length,style))
               
    def remove(self, line):
        """ Removes the given line."""
        self._lines.remove(line)
        
    def remove_lines(self, x, y):
        """ Remove all lines that pass through the given point."""
        for line in self.get_lines(x,y):
            self._lines.remove(line)
                   
    def remove_lines_rect(self, rect):
        """ Remove all lines that intersect the given rectangle, including edges."""
        raise NotImplementedError("not implemented yet")
    
    def get_lines(self, x, y):
        """ Get the lines that interect a point."""
        result = []
        for line in self._lines:
            if line.type == OrthoLine.VLINE and line.x == x:
                dist = abs(y - line.y)
            elif line.type == OrthoLine.HLINE and line.y == y:
                dist = abs(x - line.x)
            else:
                continue
                
            if dist < line.length - 1:
                result.append(line)
        return result
    
    def clear(self):
        """ Removes all lines."""
        self._lines = []
    
    #TODO: should be tested
    def _cross(self, line, other_lines):
        """ Get the points where the given line cross any line in the Lines object
            (only vertical lines can cross horizontal lines and vice versa).
            Returns a dict mapping tuples (x,y) to an intersection type "nw", "tn", "x", etc.
        """ 
        result = {}
        for other in other_lines:
            #x1, x2, y1, y2 -> endpoints of lines
            #(x,y) location of intersection
            if line.type == OrthoLine.HLINE and other.type == OrthoLine.VLINE:
                hline = line
                vline = other
            elif line.type == OrthoLine.VLINE and other.type == OrthoLine.HLINE:
                hline = other
                vline = line
            else:
                continue
            
            x1, x2 = hline.x, hline.x + hline.length - 1    #endpoints of horizontal line
            y1, y2 = vline.y, vline.y + vline.length - 1    #endpoints of vertical line
            x, y = vline.x, hline.y                         #location of intersection
            
            if (x < x1 or x2 < x) or (y < y1 or y2 < y):
                continue    #no crossing
            elif x == x1 and y == y1:   #NW corner
                result[x,y] = "nw"
            elif x == x1 and y == y2:   #SW corner
                result[x,y] = "sw"
            elif x == x2 and y == y1:   #NE corner
                result[x,y] = "ne"
            elif x == x2 and y == y2:   #SE corner
                result[x,y] = "se"
            elif y == y1 and (x1 < x and x < x2):   #T pointing S
                result[x,y] = "ts"
            elif y == y2 and (x1 < x and x < x2):   #T pointing N
                result[x,y] = "ts"
            elif x == x1 and (y1 < y and y < y2):   #T pointing E
                result[x,y] = "te"
            elif x == x2 and (y1 < y and y < y2):   #T pointing W
                result[x,y] = "tw"
            elif (x1 < x and x < x2) and (y1 < y and y < y2):   #cross
                result[x,y] = "x"
            else:
                assert False, "unhandled case: (x1=%d, x2=%d), (y1=%d, y2=%d), (x=%d, y=%d)"%(x1,x2,y1,y2,x,y)
        
        return result
        
    def __iter__(self): return iter(self._lines)
    
    def __len__(self): return len(self._lines)
           
    def paint(self, canvas):           
            #draw lines
            for line in self._lines:
                linestyle = line.style or self.default_linestyle
                if line.type == OrthoLine.HLINE:
                    canvas.hline(line.x, line.y, line.length, linestyle["h"])
                elif line.type == OrthoLine.VLINE:
                    canvas.vline(line.x, line.y, line.length, linestyle["v"])
                else:
                    raise ValueError("unknown line type: %d"%line.type)
            
            #place intersections
            lines = list(reversed(self._lines))
            while len(lines) > 1:   #one line can't cross itself
                linestyle = line.style or self.default_linestyle
                line = lines.pop()
                cross_points = self._cross(line, lines)
                for pos, cross_char in cross_points.iteritems():
                    x,y = pos
                    canvas.put_char(x,y,linestyle[cross_char])
                    
            
if __name__ == "__main__":
    
    import console
    """
    linestyle = single_line
    console.init(3,3,"Line Intersections")
    console.canvas().put_char(0,0,linestyle["nw"])
    console.canvas().put_char(1,0,linestyle["tn"])
    console.canvas().put_char(2,0,linestyle["ne"])
    console.canvas().put_char(0,1,linestyle["tw"])
    console.canvas().put_char(1,1,linestyle["x"])
    console.canvas().put_char(2,1,linestyle["te"])
    console.canvas().put_char(0,2,linestyle["sw"])
    console.canvas().put_char(1,2,linestyle["ts"])
    console.canvas().put_char(2,2,linestyle["se"])
    console.flush()
    console.wait_for_user()
    """
    
    lines = LinePainter(single_line)
    lines.add("hline", 3,3,4)
    lines.add("vline", 6,3,4)
    
    console.init(20,20,"LinePainter Test")
    console.canvas().printstr(0,0,"01234567890")
    lines.paint(console.canvas())
    console.flush()
    console.wait_for_user()