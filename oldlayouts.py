from canvas import CanvasState
from decorators import Anchor, Padding, Align

#GridLayout

class AttributeMap (object):
    """ TODO
    """
    def __init__(self, default_attrs):
        self._attrs = {}
        self._def_attrs = default_attrs  #default attributes
       
    def add(self, key, **attr):
        self._attrs[key] = attr
    
    def __getitem__(self, key_tuple):
        key, attr_name = key_tuple
        if attr_name in self._def_attrs:
            return self._attrs[key].get(attr_name, self._def_attrs[attr_name])
        return self._attrs[key][attr_name]
        
    def __setitem__(self, key_tuple, attr_val):
        key, attr_name = key_tuple
        self._attrs[key][attr_name] = attr_val
        
    def get_default(self, attr_name):
        self._def_attrs[attr_name]
    
    def set_default(self, attr_name, attr_val):
        self._def_attrs[attr_name] = attr_val
        
    def __delitem__(self, key):
        if isinstance(key, tuple):
            key, attr_name = key
            del self._attrs[key][attr_name]
        else:
            del self._attrs[key]
        
    def clear(self):
        self._attrs.clear()
        
    def iterkeys(self):
        return iter(self.keys())

    def iteritems(self):
        return iter(self.items())
        
    def keys(self):
        return self._attrs.keys()
        
    def items(self):
        return self._attrs.items()
        
    def __len__(self):
        return len(self._attrs)
        
    def __iter__(self):
        for c, attr in self._attrs.iteritems():
            d = dict(self._def_attrs)
            d.update(attr)
            yield (c, d)
    
    
class AbsoluteLayout(object):
    def __init__(self):
        defaults = {
            "zlevel": 0,
            "halign": "left",
            "valign": "top",}
        self._attrs = AttributeMap(defaults)
            
    def add(self,comp,x,y, **attr):
        """ Adds a component with the given x,y coords and zlevel.
            Components with greater zlevel are drawn on top of those 
            with a lesser zlevel. A component can be anything that has
            a render(canvas,x,y) method.
        """
        attr["pos"] = (x,y)
        self._attrs.add(comp, **attr)
    
    def remove(self, comp):
        del self._attrs[comp]
        
    def clear(self):
        self._attrs.clear()
        
    def width(self):
        if len(self) == 0: return 0
        return max([attr["pos"][0] + comp.width() for comp, attr in self._attrs]) #find rightmost component
        
    def height(self):
        if len(self) == 0: return 0
        return max([attr["pos"][1] + comp.height() for comp, attr in self._attrs]) #find bottommost component
        
    def render(self, canvas, x, y):
        items = self._attrs.keys()
        
        #highest zlevel is drawn last (on top)
        items.sort(lambda a,b: cmp(self._attrs[a, "zlevel"], self._attrs[b, "zlevel"]))
        
        with CanvasState(canvas, x, y):
            for comp in items:
                x,y = self._attrs[comp, "pos"]
                align = Align(comp, halign=self._attrs[comp,"halign"], valign=self._attrs[comp,"valign"])
                align.render_aligned(canvas, x, y)
            
class VerticalLayout(object):
    def __init__(self, min_width=0, spacing=0):
        defaults = {
            "left" : 0,
            "right" : 0,
            "halign" : "left"}
        self._attrs = AttributeMap(defaults)
        self._complist = []
        
        self.min_width = min_width
        self.spacing = spacing
    
    def add(self, comp, **attrs):
        self._complist.append(comp)
        self._attrs.add(comp,**attrs)
    
    def remove(self, comp):
        self._complist.remove(comp)
        del self._attrs[comp]
        
    def clear(self):
        self._complist[:] = []
        self._attrs.clear()
    
    def width(self):
        widths = [c.width() + attr["left"] + attr["right"] for c, attr in self._attrs]
        widths.append(self.min_width)
        return max(widths)
    
    def height(self):
        if len(self) == 0: 
            return 0
        return sum([c.height() for c in self._complist]) + self.spacing*(len(self._complist)-1)
        
    def render(self, canvas, x, y):
        width = self.width()
        with CanvasState(canvas, x, y):
            y = 0
            for comp in self._complist:
                padding = Padding(left=self._attrs[comp,"left"],
                                  right=self._attrs[comp,"right"])
                anchor = Anchor(halign=self._attrs[comp,"halign"], 
                                valign="top",
                                min_width=width)
                                
                comp = comp >> padding >> anchor
                comp.render(canvas,0,y)
                y += comp.height() + self.spacing
                
class HorizontalLayout(object):
    def __init__(self, min_height=0, spacing=0):
        defaults = {
            "top" : 0,
            "bottom" : 0,
            "valign" : "top"}
        self._attrs = AttributeMap(defaults)
        self._complist = []
        
        self.min_height = min_height
        self.spacing = spacing
    
    def add(self, comp, **attrs):
        self._complist.append(comp)
        self._attrs.add(comp,**attrs)
    
    def remove(self, comp):
        self._complist.remove(comp)
        del self._attrs[comp]
        
    def clear(self):
        self._complist[:] = []
        self._attrs.clear()
    
    def width(self):
        if len(self) == 0: 
            return 0
        return sum([c.width() for c in self._complist]) + self.spacing*(len(self._complist)-1)
    
    def height(self):
        heights = [c.height() + self.attr["top"] + self.attr["bottom"] for c, attr in self._attrs]
        heights.append(self.min_height)
        return max(heights)
        
    def render(self, canvas, x, y):
        height = self.height()
        with CanvasState(canvas, x, y):
            x = 0
            for comp in self._complist:
                padding = Padding(top=self._attrs[comp,"top"],
                                  bottom=self._attrs[comp,"bottom"])
                anchor = Anchor(halign="left", 
                                valign=self._attrs[comp,"valign"],
                                min_height=height)
                                
                comp = comp >> padding >> anchor
                comp.render(canvas,x,0)
                x += comp.width() + self.spacing
                
class GridLayout (object):
    def __init__ (self, num_cols, num_rows):
        defaults = {
            "valign" : "center",
            "halign" : "center",}
        self.num_cols = num_cols
        self.num_rows = num_rows
        self._attrs = AttributeMap(defaults)
        self._content = {}  #map col,row locations to component
    
    def add (self, comp, col, row, **attrs):
        if (col,row) in self._content:
            del self._attrs[self._content[col,row]]
        
        self._content[col,row] = comp
        self._attrs.add(comp, **attrs)
    
    def remove (self, col, row):
        comp = self._content.get((col,row), None)
        if comp:
            del self._content[col,row]
            del self._attrs[comp]
    
    def clear (self):
        self._content.clear()
        self._attrs.clear()
    
    
    
        
    