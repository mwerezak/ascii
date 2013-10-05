""" This module defines the Colour object and many default colours.
    
    Several string representation of Colour objects are supported: these are hex strings, csv strings, and name strings.
        Hex strings have the form "#RRGGBB", where RR,GG,BB are hex values from 0 - 255 and are exactly 2 characters long.
        CSV strings have the form "r,g,b", where r, g, and b are either a decimal integer or a hex integer following a '#' e.g. #FF
        Name strings can be any key string from the colour_names property.
    
    TODO: HSV support?
"""

import libtcodpy as dlib

def from_hex (colour_str):
    if colour_str[0] == '#':    #remove optional '#'
        colour_str = colour_str[1:]
    
    r = int(colour_str[0:2], 16)
    g = int(colour_str[2:4], 16)
    b = int(colour_str[4:6], 16)
    
    return Colour(r,g,b)

def from_name (name_str):
    """ Creates a new Colour that is a copy of the Colour indicated by name_str. """
    if name_str in colour_names:
        return Colour(*colour_names[name_str])
    raise KeyError("'%s' is not a recognized colour name"%name_str)

def from_csv (csv_str):
    """ Attempts to create a new Colour from a comma-separated list of values r, g, b.
        r, g, and b can be either a decimal integer or a hex value starting with #
    """
    str_values = csv_str.split(",", 2)
    values = []
    for s in str_values:
        if s[0] == '#':
            values.append(int(s[1:], 16))
        else:
            values.append(int(s))
    return Colour(*values)
    
def from_str (s):
    """ Attempts to parse a string into a Colour object. """
    try: 
        return from_csv(s)
    except Exception: 
        pass
        
    try: 
        return from_hex(s)
    except Exception: 
        pass

    try:
        return from_name(s)
    except Exception: 
        pass

    raise ColourFormatError("'%s' is not a recognized colour string"%s)

class ColourFormatError (Exception): pass
       
#originaly _TCODColour
class Colour (object):
    """ Wrapper over a LibTCOD Color object
    """
    def __init__(self, r, g, b, struct=None):
        """ r, g, b are the RGB values of the colour between 0 and 255. If struct is provided, these are ignored.
            struct is the LibTCOD Color struct to be used for this colour.
        """
        self._intern = struct or dlib.Color(r,g,b)
    
    def hex_str (self):
        """ Returns the hex-string representation of this colour. """
        return "#%02X%02X%02X"%(self._intern[0],self._intern[1],self._intern[2])
        
    def get_struct (self):
        """ Returns the internal LibTCOD implementation of this colour. """
        return self._intern
        
    def __eq__ (self, other):
        return self._intern == other._intern

    def __add__ (self, other):
        return Colour(*(self._intern + other._intern))
    
    def __sub__ (self, other):
        return Colour(*(self._intern - other._intern))
    
    def __mul__ (self, other):
        if isinstance(other, self.__class__):
            return Colour(*(self._intern * other._intern))
        return self._scalar_mult(other)
    
    def __rmul__ (self, other):
        return self * other
        
    def _scalar_mult (self, n):
        return Colour(0,0,0, self._intern * n)
        
    def __iter__(self):
        """ Produces an iterator over the components of this colour. """
        return iter(self._intern)
    
    def __repr__(self):
        return "%s%s"%(self.__class__.__name__, tuple(self._intern))
    
#Not used
class _RGBColour (object):
    """ Simple data structure for an RGB colour.
    """
    def __init__(self, r, g, b):
        """ r, g, b are the RGB values of the colour between 0 and 255.
            To copy a Colour object, simply use Colour(*other_colour)
        """
        if r < 0 or r > 255: raise ValueError("r value is out of range: %d"%r)
        if g < 0 or g > 255: raise ValueError("g value is out of range: %d"%g)
        if b < 0 or b > 255: raise ValueError("b value is out of range: %d"%b)
        
        self.r, self.g, self.b = r, g, b
    
    def hex_str (self):
        """ Returns the hex-string representation of this colour. """
        return "#%02X%02X%02X"%(self.r, self.g, self.b)
        
    def __eq__ (self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b
    
    def __iter__(self):
        """ Produces an iterator over the components of this colour. """
        return iter((self.r, self.g, self.b))
    
    def __repr__(self):
        return "%s(%d,%d,%d)"%(self.__class__.__name__, self.r, self.g, self.b)

class TextColourParser (object):
    """ 
    """
    pass
    
## Initialization
colour_names = {}       #A dictionary that will contain the default colours
#Colour = _TCODColour    #define the default Colour implementation
        
#######################################################################
## Default Colours
#######################################################################

# grey levels

black=Colour(0,0,0)
darkest_grey=Colour(31,31,31)
darker_grey=Colour(63,63,63)
dark_grey=Colour(95,95,95)
grey=Colour(127,127,127)
light_grey=Colour(159,159,159)
lighter_grey=Colour(191,191,191)
lightest_grey=Colour(223,223,223)
darkest_gray=Colour(31,31,31)
darker_gray=Colour(63,63,63)
dark_gray=Colour(95,95,95)
gray=Colour(127,127,127)
light_gray=Colour(159,159,159)
lighter_gray=Colour(191,191,191)
lightest_gray=Colour(223,223,223)
white=Colour(255,255,255)

# sepia
darkest_sepia=Colour(31,24,15)
darker_sepia=Colour(63,50,31)
dark_sepia=Colour(94,75,47)
sepia=Colour(127,101,63)
light_sepia=Colour(158,134,100)
lighter_sepia=Colour(191,171,143)
lightest_sepia=Colour(222,211,195)

#standard Colours
red=Colour(255,0,0)
flame=Colour(255,63,0)
orange=Colour(255,127,0)
amber=Colour(255,191,0)
yellow=Colour(255,255,0)
lime=Colour(191,255,0)
chartreuse=Colour(127,255,0)
green=Colour(0,255,0)
sea=Colour(0,255,127)
turquoise=Colour(0,255,191)
cyan=Colour(0,255,255)
sky=Colour(0,191,255)
azure=Colour(0,127,255)
blue=Colour(0,0,255)
han=Colour(63,0,255)
violet=Colour(127,0,255)
purple=Colour(191,0,255)
fuchsia=Colour(255,0,255)
magenta=Colour(255,0,191)
pink=Colour(255,0,127)
crimson=Colour(255,0,63)

# dark Colours
dark_red=Colour(191,0,0)
dark_flame=Colour(191,47,0)
dark_orange=Colour(191,95,0)
dark_amber=Colour(191,143,0)
dark_yellow=Colour(191,191,0)
dark_lime=Colour(143,191,0)
dark_chartreuse=Colour(95,191,0)
dark_green=Colour(0,191,0)
dark_sea=Colour(0,191,95)
dark_turquoise=Colour(0,191,143)
dark_cyan=Colour(0,191,191)
dark_sky=Colour(0,143,191)
dark_azure=Colour(0,95,191)
dark_blue=Colour(0,0,191)
dark_han=Colour(47,0,191)
dark_violet=Colour(95,0,191)
dark_purple=Colour(143,0,191)
dark_fuchsia=Colour(191,0,191)
dark_magenta=Colour(191,0,143)
dark_pink=Colour(191,0,95)
dark_crimson=Colour(191,0,47)

# darker Colours
darker_red=Colour(127,0,0)
darker_flame=Colour(127,31,0)
darker_orange=Colour(127,63,0)
darker_amber=Colour(127,95,0)
darker_yellow=Colour(127,127,0)
darker_lime=Colour(95,127,0)
darker_chartreuse=Colour(63,127,0)
darker_green=Colour(0,127,0)
darker_sea=Colour(0,127,63)
darker_turquoise=Colour(0,127,95)
darker_cyan=Colour(0,127,127)
darker_sky=Colour(0,95,127)
darker_azure=Colour(0,63,127)
darker_blue=Colour(0,0,127)
darker_han=Colour(31,0,127)
darker_violet=Colour(63,0,127)
darker_purple=Colour(95,0,127)
darker_fuchsia=Colour(127,0,127)
darker_magenta=Colour(127,0,95)
darker_pink=Colour(127,0,63)
darker_crimson=Colour(127,0,31)

# darkest Colours
darkest_red=Colour(63,0,0)
darkest_flame=Colour(63,15,0)
darkest_orange=Colour(63,31,0)
darkest_amber=Colour(63,47,0)
darkest_yellow=Colour(63,63,0)
darkest_lime=Colour(47,63,0)
darkest_chartreuse=Colour(31,63,0)
darkest_green=Colour(0,63,0)
darkest_sea=Colour(0,63,31)
darkest_turquoise=Colour(0,63,47)
darkest_cyan=Colour(0,63,63)
darkest_sky=Colour(0,47,63)
darkest_azure=Colour(0,31,63)
darkest_blue=Colour(0,0,63)
darkest_han=Colour(15,0,63)
darkest_violet=Colour(31,0,63)
darkest_purple=Colour(47,0,63)
darkest_fuchsia=Colour(63,0,63)
darkest_magenta=Colour(63,0,47)
darkest_pink=Colour(63,0,31)
darkest_crimson=Colour(63,0,15)

# light Colours
light_red=Colour(255,114,114)
light_flame=Colour(255,149,114)
light_orange=Colour(255,184,114)
light_amber=Colour(255,219,114)
light_yellow=Colour(255,255,114)
light_lime=Colour(219,255,114)
light_chartreuse=Colour(184,255,114)
light_green=Colour(114,255,114)
light_sea=Colour(114,255,184)
light_turquoise=Colour(114,255,219)
light_cyan=Colour(114,255,255)
light_sky=Colour(114,219,255)
light_azure=Colour(114,184,255)
light_blue=Colour(114,114,255)
light_han=Colour(149,114,255)
light_violet=Colour(184,114,255)
light_purple=Colour(219,114,255)
light_fuchsia=Colour(255,114,255)
light_magenta=Colour(255,114,219)
light_pink=Colour(255,114,184)
light_crimson=Colour(255,114,149)

#lighter Colours
lighter_red=Colour(255,165,165)
lighter_flame=Colour(255,188,165)
lighter_orange=Colour(255,210,165)
lighter_amber=Colour(255,232,165)
lighter_yellow=Colour(255,255,165)
lighter_lime=Colour(232,255,165)
lighter_chartreuse=Colour(210,255,165)
lighter_green=Colour(165,255,165)
lighter_sea=Colour(165,255,210)
lighter_turquoise=Colour(165,255,232)
lighter_cyan=Colour(165,255,255)
lighter_sky=Colour(165,232,255)
lighter_azure=Colour(165,210,255)
lighter_blue=Colour(165,165,255)
lighter_han=Colour(188,165,255)
lighter_violet=Colour(210,165,255)
lighter_purple=Colour(232,165,255)
lighter_fuchsia=Colour(255,165,255)
lighter_magenta=Colour(255,165,232)
lighter_pink=Colour(255,165,210)
lighter_crimson=Colour(255,165,188)

# lightest Colours
lightest_red=Colour(255,191,191)
lightest_flame=Colour(255,207,191)
lightest_orange=Colour(255,223,191)
lightest_amber=Colour(255,239,191)
lightest_yellow=Colour(255,255,191)
lightest_lime=Colour(239,255,191)
lightest_chartreuse=Colour(223,255,191)
lightest_green=Colour(191,255,191)
lightest_sea=Colour(191,255,223)
lightest_turquoise=Colour(191,255,239)
lightest_cyan=Colour(191,255,255)
lightest_sky=Colour(191,239,255)
lightest_azure=Colour(191,223,255)
lightest_blue=Colour(191,191,255)
lightest_han=Colour(207,191,255)
lightest_violet=Colour(223,191,255)
lightest_purple=Colour(239,191,255)
lightest_fuchsia=Colour(255,191,255)
lightest_magenta=Colour(255,191,239)
lightest_pink=Colour(255,191,223)
lightest_crimson=Colour(255,191,207)

# desaturated Colours
desaturated_red=Colour(127,63,63)
desaturated_flame=Colour(127,79,63)
desaturated_orange=Colour(127,95,63)
desaturated_amber=Colour(127,111,63)
desaturated_yellow=Colour(127,127,63)
desaturated_lime=Colour(111,127,63)
desaturated_chartreuse=Colour(95,127,63)
desaturated_green=Colour(63,127,63)
desaturated_sea=Colour(63,127,95)
desaturated_turquoise=Colour(63,127,111)
desaturated_cyan=Colour(63,127,127)
desaturated_sky=Colour(63,111,127)
desaturated_azure=Colour(63,95,127)
desaturated_blue=Colour(63,63,127)
desaturated_han=Colour(79,63,127)
desaturated_violet=Colour(95,63,127)
desaturated_purple=Colour(111,63,127)
desaturated_fuchsia=Colour(127,63,127)
desaturated_magenta=Colour(127,63,111)
desaturated_pink=Colour(127,63,95)
desaturated_crimson=Colour(127,63,79)

# metallic
brass=Colour(191,151,96)
copper=Colour(197,136,124)
gold=Colour(229,191,0)
silver=Colour(203,203,203)

# miscellaneous
celadon=Colour(172,255,175)
peach=Colour(255,159,127)

#build a dictionary of the colours contained in this module
_global_dict = dict(globals())
for name, val in _global_dict.iteritems():
    if isinstance(val, Colour):
        colour_names[name] = val
