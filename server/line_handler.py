import re
from common.dbus_message import DbusMessage

class LineHandler:
    def __init__(self):
        self.current_message = None

    ##
    # Lines printed by dbus-monitor that start with no spaces are the header
    # line of a message.  Lines that start with 3 spaces are part of the 
    # body of a message.  During parsing, when a header line is detected
    # we should consider the last message complete.
    #
    def handle_line(self, line):
        if re.match('^\s{3,}\S+.*', line):
            if self.current_message:
                self.current_message.add_line(line)
        else:
            complete_msg = self.current_message
            if complete_msg:
                complete_msg.parse()
            self.current_message = DbusMessage(line)
            return complete_msg
