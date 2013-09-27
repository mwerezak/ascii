
#Never assume something is faster with more threads

class EventSource (object):
    def __init__ (self):
        self._callbacks = []
    
    def register (self, callback):
        self._callbacks.append(callback)
        
    def remove (self, callback):
        self._callbacks.remove(callback)
    
    def clear (self):
        self._callbacks.clear()
        
    def fire (self, origin, *args):
        for callback in self._callbacks:
            callback(origin, *args)
        
        
"""
class EventSource (object):
    def __init__ (self):
        self.callbacks = {}
        
    def register(self, type, callback):
        call_set = self.callbacks.setdefault(type, set())
        call_set.add(callback)
    
    def remove(self, type, callback):
        if type in self.callbacks:
            self.callbacks[type].discard(callback)
    
    def remove_all(self, type):
        if type in self._callbacks:
            del self.callbacks[type]
        
    def fire_event(self, type, *args):
        if type in self.callbacks:
            call_set = self.callbacks[type]
            for callback in call_set:
                callback(self, type, *args)
"""