import select

#
# Returns whether the specified socket is ready to be read from.
#
def ready_for_read(socket):
    rv = select.select([socket], [], [], 0.1)
    return len(rv[0]) > 0
