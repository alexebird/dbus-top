import select
import Queue

global_msg_queue = Queue.Queue()

#
# Returns whether the specified socket is ready to be read from.
#
def ready_for_read(socket):
    return socket in select.select([socket], [], [], 0.1)[0]
