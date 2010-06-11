import re
from dbus_message import *

class LineHandler:
    current_message = None

    @staticmethod
    def handle_line(line):
        if re.match('^\s{3,}\S+.*', line):
            if LineHandler.current_message:
                LineHandler.current_message.add_line(line)
        else:
            complete_msg = LineHandler.current_message
            if complete_msg:
                complete_msg.parse()
            LineHandler.current_message = DbusMessage(line)
            return complete_msg
