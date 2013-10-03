
from blist import sorteddict
import libtcodpy as dlib


class Animation (object):
    """ An animation consists of a sequence of frames, each with a duration in ticks.
        Each frame is a widget, and the Animation object is itself a widget that simply
        renders as whatever the current frame is.
        The meaning of a tick is determined by the clock implementation used.
    """
    
    def __init__ (self, frames, clock, loop=True):
        """ frames should be a sequence of (widget, duration).
            clock should be an object that has a get_tick() method.
            If loop is True, then the Animation will reset once the last frame's duration passes.
        """
        if len(frames) == 0:
            raise ValueError ("at least one frame must be supplied")
        
        self.frames = list(frames)
        self.clock = clock
        self.loop = loop
        
        self.reset()
        
    def reset (self): 
        self._cur_idx = 0
        self._cur_frame, self._next_frame_tick = self.frames[0]
        self._start_tick = self.clock.get_tick()
    
    def update (self):
        cur_tick = self.clock.get_tick() - self._start_tick
        
        while cur_tick >= self._next_frame_tick:
            
            #check if we are at the last frame
            if self._cur_idx >= len(self.frames) - 1:
                if self.loop: self.reset()
                return
            
            self._cur_idx += 1
            self._cur_frame, next_frame_duration = self.frames[self._cur_idx]
            self._next_frame_tick += next_frame_duration           
        
    def current_frame (self):
        return self._cur_frame
    
    def set_current_frame (self, idx):
        if idx == 0:
            self.reset()
            return
        
        if idx < 0:
            idx = len(self.frames) - idx
        if idx >= len(self.frames):
            raise IndexError ("index out of range")
        
        self._cur_idx = idx
        self._cur_frame = self.frames[idx]
        
        durations = zip(*self.frames)[1]
        self._next_frame_tick = sum(durations[:idx])
        self._start_tick = self.clock.get_tick() - sum(durations[:idx - 1])
    
    def seek (self, ticks):
        """ Similar to set_current_frame(), but sets the Animation as if the specified 
            number of ticks has elapsed since start.
        """
        elapsed_duration = 0
        for i, (frame, duration) in enumerate(self.frame):
            if ticks < elapsed_duration + duration: break
        
        self.set_current_frame(i)
        self._start_tick = self.clock.get_tick() - ticks
    
    def extend (self, other):
        self.frames.extend(other)
        
    def __iter__ (self):
        return iter(self.frames)
    
    def width (self): return self._cur_frame.width()
        
    def height (self): return self._cur_frame.height()
    
    def render(self, canvas, x, y): 
        self._cur_frame.render(canvas, x, y)
        
        
class ProgramClock (object):
    """ A clock that provides the number of milliseconds elapsed since
        the program has started.
    """
    def get_tick(self):
        return dlib.sys_elapsed_milli()

## Test Code
if __name__ == "__main__":
    pass
