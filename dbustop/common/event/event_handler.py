import Queue

#class EventHandler:

__event_queue = Queue.Queue()

def add_event(new_event):
    __event_queue.put(new_event)

def next_event():
    try:
        return __event_queue.get(True, 0.1)
    except Queue.Empty:
        return None
