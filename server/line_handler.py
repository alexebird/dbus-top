import re
from common import dbus_message

class LineHandler:
    def __init__(self):
        self.current_message = None

    def handle_line(self, line):
        if re.match('^\s{3,}\S+.*', line):
            if self.current_message:
                self.current_message.add_line(line)
        else:
            complete_msg = self.current_message
            if complete_msg:
                complete_msg.parse()
            self.current_message = dbus_message.DbusMessage(line)
            return complete_msg
