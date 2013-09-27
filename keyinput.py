import libtcodpy as dlib
from events import EventSource
import console

_keycodes = [
    (dlib.KEY_NONE,     ""),
    (dlib.KEY_ESCAPE,   "esc"),
    (dlib.KEY_BACKSPACE,"back"),
    (dlib.KEY_TAB,      "tab"),
    (dlib.KEY_ENTER,    "enter"),
    (dlib.KEY_SHIFT,    "shift"),
    (dlib.KEY_CONTROL,  "ctrl"),
    (dlib.KEY_ALT,      "alt"),
    (dlib.KEY_PAUSE,    "pause"),
    (dlib.KEY_CAPSLOCK, "caps"),
    (dlib.KEY_PAGEUP,   "pgup"),
    (dlib.KEY_PAGEDOWN, "pgdown"),
    (dlib.KEY_END,      "end"),
    (dlib.KEY_HOME,     "home"),
    (dlib.KEY_UP,       "up"),
    (dlib.KEY_LEFT,     "left"),
    (dlib.KEY_RIGHT,    "right"),
    (dlib.KEY_DOWN,     "down"),
    (dlib.KEY_PRINTSCREEN, "printscn"),
    (dlib.KEY_INSERT,   "ins"),
    (dlib.KEY_DELETE,   "del"),
    (dlib.KEY_LWIN,     "lmeta"),
    (dlib.KEY_RWIN,     "rmeta"),
    (dlib.KEY_APPS,     "apps"),
    (dlib.KEY_0,        "0"),
    (dlib.KEY_1,        "1"),
    (dlib.KEY_2,        "2"),
    (dlib.KEY_3,        "3"),
    (dlib.KEY_4,        "4"),
    (dlib.KEY_5,        "5"),
    (dlib.KEY_6,        "6"),
    (dlib.KEY_7,        "7"),
    (dlib.KEY_8,        "8"),
    (dlib.KEY_9,        "9"),
    (dlib.KEY_KP0,      "kp0"),
    (dlib.KEY_KP1,      "kp1"),
    (dlib.KEY_KP2,      "kp2"),
    (dlib.KEY_KP3,      "kp3"),
    (dlib.KEY_KP4,      "kp4"),
    (dlib.KEY_KP5,      "kp5"),
    (dlib.KEY_KP6,      "kp6"),
    (dlib.KEY_KP7,      "kp7"),
    (dlib.KEY_KP8,      "kp8"),
    (dlib.KEY_KP9,      "kp9"),
    (dlib.KEY_KPADD,    "kp+"),
    (dlib.KEY_KPSUB,    "kp-"),
    (dlib.KEY_KPDIV,    "kp/"),
    (dlib.KEY_KPMUL,    "kp*"),
    (dlib.KEY_KPDEC,    "kp."),
    (dlib.KEY_KPENTER,  "kpenter"),
    (dlib.KEY_F1,       "f1"),
    (dlib.KEY_F2,       "f2"),
    (dlib.KEY_F3,       "f3"),
    (dlib.KEY_F4,       "f4"),
    (dlib.KEY_F5,       "f5"),
    (dlib.KEY_F6,       "f6"),
    (dlib.KEY_F7,       "f7"),
    (dlib.KEY_F8,       "f8"),
    (dlib.KEY_F9,       "f9"),
    (dlib.KEY_F10,      "f10"),
    (dlib.KEY_F11,      "f11"),
    (dlib.KEY_F12,      "f12"),
    (dlib.KEY_NUMLOCK,   "num"),
    (dlib.KEY_SCROLLLOCK,"scroll"),
    (dlib.KEY_SPACE,     "space"),
    (dlib.KEY_CHAR,      None),
]

_keycode_dict = dict(_keycodes)
_keyid_dict = dict(zip(*reversed(zip(*_keycodes))))

def keycode(key_id):
    """Takes a Lib TCOD key id (an int) and returns a str keycode."""
    if key_id not in _keycode_dict:
        raise ValueError("unmapped key id: %d"%key_id)
    return _keycode_dict[key_id]
    
def ord_key(keycode):
    """Returns the int representing the keycode in Lib TCOD."""
    if keycode not in _keyid_dict:
        raise ValueError("unmapped keycode: %s"%keycode)
    return _keyid_dict[keycode]

def is_keycode(keycode):
    if keycode is None:
        return False
    return keycode in _keyid_dict
       
class Keypress(object):
    """ syntax for a Keypress string: meta+keycode
        e.g. ctrl+shift+space
    """
    def __init__(self, keypress):
        if isinstance(keypress, basestring):
            self._init_from_str(keypress)
        else:
            self._init_from_struct(keypress)
        
    def _init_from_struct(self, struct):
        """    init using a Lib TCOD keypress struct."""
        self.code = keycode(struct.vk)      #code used to uniquely identify the keypress (excluding metakeys)
        if self.code is None:
            self.code = chr(struct.c).lower()
        
        if struct.c:
            self.printch = chr(struct.c)    #holds the printable representation of a keypress for use with raw text input controls, e.g. text box
        else:
            self.printch = None
        
        self._metas = set()                #metakeys
        if struct.lalt: self._metas.add("lalt")
        if struct.lctrl: self._metas.add("lctrl")
        if struct.ralt: self._metas.add("ralt")
        if struct.rctrl: self._metas.add("rctrl")
        if struct.shift: self._metas.add("shift")
        
        self.released = not struct.pressed       #whether the struct was a key press or key release. Not used for comparisons
        
    def _init_from_str(self, string):
        """Parse a string into a Keypress object."""
        split = string.split("+")
        if len(split) == 1:
            metas = []
            keycode = split[0]
        else:
            metas = split[:-1]
            keycode = split[-1]
            #handle "meta++" special case (e.g. alt++, alt and the '+' key)
            if len(metas) >= 1 and metas[-1] == "" and keycode == "":
                metas.pop()
                keycode = "+"
            
        #metakeys
        self._metas = set([meta.lower() for meta in metas])
            
        if is_keycode(keycode):
            self.code = keycode
            self.printch = None
        else:
            #uppercase char shortcut
            if len(keycode) == 1 and keycode.isupper():
                self._metas.add("shift")
            self.code = keycode.lower()                
            self.printch = keycode
        
        self.released = None
        
    @property
    def pressed(self):
        return self.released is not None and not self.released
        
    def has_meta(self, meta):
        """Returns True if this Keypress has the given meta-key in it's keypress combination."""
        if meta in self._metas:
            return True
    
        if meta == "alt":
            return "lalt" in self._metas or "ralt" in self._metas
        if (meta == "lalt" or meta == "ralt") and "alt" in self._metas:
            return True
            
        if meta == "ctrl":
            return "lctrl" in self._metas or "rctrl" in self._metas
        if (meta == "lctrl" or meta == "rctrl") and "ctrl" in self._metas:
            return True
            
        return False
           
    def __eq__(self, other): 
        if isinstance(other, Keypress):
            for meta in self._metas ^ other._metas:
                if not self.has_meta(meta) or not other.has_meta(meta):
                    return False
            return self.code == other.code
        
        return self == Keypress(other)
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __repr__(self):
        if len(self._metas):
            meta = ", metas=%s"%self._metas 
        else:
            meta = ""
        
        return '<%s.Keypress object: code=%s, printch="%s"%s>'%(self.__module__, self.code, self.printch, meta)
        
    def __str__(self):
        if len(self._metas):
            metas = "+".join(self._metas) + "+"
        else:
            metas = ""
        s = "%s%s"%(metas, self.code)
        assert self == s, "keycode string not equal to Keypress: " + s
        return s
            

## Keyboard Input Functions
            
def get_input_blocking (flush=True):
    key_struct = dlib.console_wait_for_keypress(flush)
    return Keypress(key_struct)

def get_input ():
    key_struct = dlib.console_check_for_keypress(dlib.KEY_PRESSED|dlib.KEY_RELEASED)
    return Keypress(key_struct)

    

## tests
if __name__ == "__main__":
    pass
    
