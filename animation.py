
class Animation (object):
    """ An animation consists of a sequence of frames, each with a duration in ticks.
        Each frame is a widget, and the Animation object is itself a widget that simply
        renders as whatever the current frame is.
        The meaning of a tick is determined by whoever calls the update() method on the animation.
    """
    
    def __init__ (self, frames, loop=True):
        """ frames should be a sequence of (widget, duration).
            clock should be an object that has a get_tick() method.
            If loop is True, then the Animation will reset once the last frame's duration passes.
        """
        if len(frames) == 0:
            raise ValueError ("at least one frame must be supplied")
        
        self.loop = loop
        
        self._cur_frame_idx = 0
        self._frames = [] #stores tuples of (start_tick, end_tick, frame). start_tick and end_tick form a half-open interval
        self.extend(frames)
        
    def reset (self): 
        self.update(0)
    
    def update (self, cur_tick):
        if self.loop:
            cur_tick %= self.total_length()
        
        for idx, (start, end, frame) in enumerate(self._frames):
            if start <= cur_tick and cur_tick < end:
                self._cur_frame_idx = idx
                return
        
        #if we got here then we've run past the end of the animation
        self._cur_frame_idx = len(self._frames) - 1
        
    def current_frame (self):
        return self._frames[self._cur_frame_idx][2]
    
    def total_length (self):
        """ Returns the total duration of the animation in ticks.
        """
        if len(self._frames) == 0:
            return 0
        return self._frames[-1][1]
        
    def extend (self, other):
        start_tick = self.total_length()
        for frame, duration in frames:
            frame_info = (start_tick, start_tick + duration, frame)
            self._frames.append(frame_info)
            start_tick += duration
        
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
