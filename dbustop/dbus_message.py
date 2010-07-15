import shlex
import re

def parse(message_str):
    if message_str.startswith('sig'):
        return __parse_signal(message_str)
    elif message_str.startswith('mc'):
        return __parse_method_call(message_str)
    elif message_str.startswith('mr'):
        return __parse_method_return(message_str)
    elif message_str.startswith('err'):
        return __parse_error(message_str)

def __tokenize_message(message_str):
    return shlex.split(message_str)

def __timestamp_in_sec(sec, usec):
    USEC_IN_SEC = 1000000
    return sec + (usec / USEC_IN_SEC)

def __parse_signal(message_str):
    tokens = __tokenize_message(message_str)
    type = tokens[0]
    sec = float(tokens[1])
    usec = float(tokens[2])
    msg = SignalMessage(type, __timestamp_in_sec(sec, usec), message_str)
    msg.serial = int(tokens[3])
    msg.object = tokens[4]
    msg.interface = tokens[5]
    msg.member = tokens[6]
    return msg

def __parse_method_call(message_str):
    tokens = __tokenize_message(message_str)
    type = tokens[0]
    sec = float(tokens[1])
    usec = float(tokens[2])
    msg = MethodCallMessage(type, __timestamp_in_sec(sec, usec), message_str)
    msg.serial = int(tokens[3])
    msg.sender = tokens[4]
    msg.object = tokens[5]
    msg.interface = tokens[6]
    msg.member = tokens[7]
    return msg

def __parse_method_return(message_str):
    tokens = __tokenize_message(message_str)
    type = tokens[0]
    sec = float(tokens[1])
    usec = float(tokens[2])
    msg = MethodReturnMessage(type, __timestamp_in_sec(sec, usec), message_str)
    msg.serial = int(tokens[3])
    msg.reply_serial = int(tokens[4])
    msg.destination = tokens[5]
    return msg

def __parse_error(message_str):
    tokens = __tokenize_message(message_str)
    type = tokens[0]
    sec = float(tokens[1])
    usec = float(tokens[2])
    msg = ErrorMessage(type, __timestamp_in_sec(sec, usec), message_str)
    msg.serial = int(tokens[3])
    msg.reply_serial = int(tokens[4])
    msg.destination = tokens[5]
    return msg

# Packet header format:
#   * int in network byte-order (big-endian)
PACKET_HEADER_FORMAT = '!i'
PACKET_HEADER_SIZE = 4  # bytes

class DbusMessage:
    def __init__(self, type, timestamp, original_text):
        self.original_text = original_text
        self.timestamp = timestamp
        self.message_type = type

class SignalMessage(DbusMessage):
    def __str__(self):
        return '%s %f %d %s %s %s' % ('signal', self.timestamp, self.serial, self.object, self.interface, self.member)

    #def json_str(self):


class MethodCallMessage(DbusMessage):
    def __str__(self):
        return '%s %f %d %s %s %s %s' % ('method_call', self.timestamp, self.serial, self.sender, self.object, self.interface, self.member)

class MethodReturnMessage(DbusMessage):
    def __str__(self):
        return '%s %f %d %d %s' % ('method_return', self.timestamp, self.serial, self.reply_serial, self.destination)

class ErrorMessage(DbusMessage):
    def __str__(self):
        return '%s %f %d %d %s' % ('error', self.timestamp, self.serial, self.reply_serial, self.destination)
