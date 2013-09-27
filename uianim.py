
from blist import sorteddict
import libtcodpy as dlib


class Animation (object):
    """
    An Animation is a type of widget that will render differently 
    depending on the value returned from its clock's get_tick() method.
    The Animation object is configured with a collection of keyframes,
    each of which has a number. The highest keyframe that is less than
    or equal to the value returned from clock.get_tick() is displayed.
      
    A frame is any widget. A clock can be any object that has a 
    get_tick() method.
    """
    
    def __init__ (self, keyframes, clock=None, loop=0):
        """
        keyframes should be a mapping type or list of tuples that 
        associates numbers integers to frames.
        If loop is positive, the Animation will restart once it reached
        that keyframe number and all of the other frames have played.
        If not set, clock will default to a ProgramClock instance.
        """
        if len(keyframes) == 0:
            raise ValueError("keyframes must have at least one item")
        
        self.clock = clock or ProgramClock()
        self.loop = loop
        self._keyframes = sorteddict(keyframes).items()
        self._startkey = self._keyframes[0][0]
        
        self._idx = 0
        self._start_tick = clock.get_tick()
        
    def _curframe(self):
        """ Get the current frame. """
        return self._keyframes[self._idx][1]
        
    def reset (self):
        self._idx = 0
        self._start_tick = clock.get_tick()
        
    def update_frame (self):
        tick = self.clock.get_tick() - self._start_tick + self._startkey
        
        #check for looping
        if loop > 0 and tick >= loop:
            self.restart()
            return
        
        for i, pair in enumerate(self._keyframes[self._idx + 1:]):
            keynum, keyframe = pair
            if keynum > tick : 
                break   #haven't reached this frame yet
            self._idx = i
    
    def width (self): return self._curframe().width()
        
    def height (self): return self._curframe.().height()
    
    def render(self, canvas, x, y): 
        self._curframe().render(canvas, x, y)
        
        
class ProgramClock (object):
    """ A clock that provides the number of milliseconds elapsed since
        the program has started.
    """
    def get_tick(self):
        return dlib.sys_elapsed_milli()
        