import shlex
import struct
import re
import pickle

# Packet header format:
#   * int in network byte-order (big-endian)
packet_header_format = '!i'
packet_header_size = 4  # bytes

class DbusMessage:
    def __init__(self, header_line):
        self.header_line = header_line
        self.parse()

    def __repr__(self):
        h = self.header
        return '<DbusMessage: msg-type=%s, sender=%s, dest=%s, member=%s>' % (h['message_type'], h['sender'], h['dest'], h['member'])

    def __str__(self):
        h = self.header
        keys = ['message_type', 'sender', 'dest', 'member']
        try:
            s_val = '(%4s) | ' % h['serial']
        except KeyError:
            s_val = '(%4s) | ' % ' '
        for k in keys:
            try:
                v = h[k]
            except KeyError:
                v = ''
            s_val += '%s=%-12s | ' % (k, v[0:12])
        return s_val.strip()

    def parse(self):
        tokens = shlex.split(self.header_line)
        key_value_re = re.compile('\S+=[^=\s]+')
        arrow_re = re.compile('->')
        curr_header_entry = ''
        header_entries = {}
        for t in tokens:
            # Skip the '->' in the header
            if arrow_re.match(t):
                continue
            # Text not matching the 'key=value' pattern
            elif key_value_re.match(t) == None:
                curr_header_entry += ' ' + t
                i = tokens.index(t)
                if (key_value_re.match(tokens[i + 1]) or i + 1 >= len(tokens)) and len(header_entries) == 0:
                    header_entries['message_type'] = curr_header_entry.strip()
                elif key_value_re.match(curr_header_entry):
                    key, value = curr_header_entry.split('=', 1)
                    header_entries[key.strip()] = value.strip()
            # Text containing a '=' is appended to the previous key's value 
            else:
                curr_header_entry = t
                key, value = curr_header_entry.split('=', 1)
                header_entries[key.strip()] = value.strip()
        self.header = header_entries

    #
    # Serialize the DbusMessage to be sent over a network stream using pickle, but
    # prepend the length of the pickle dump.  Returns the length as an int byte string
    # form plus the pickle dump string itself.
    #
    def packetize(self):
        data = pickle.dumps(self)
        length_bytes = struct.pack(packet_header_format, len(data))
        return length_bytes + data

#
# Reads and serializes a python DbusMessage object from the specified socket.
#
def depacketize(sock):
    pkt_size_str = sock.recv(packet_header_size)
    # unpack() returns a tuple even if only one item is unpacked, thus the [0].
    pkt_size = struct.unpack(packet_header_format, pkt_size_str)[0]
    serialized_dbus_msg = sock.recv(pkt_size)
    try:
        msg = pickle.loads(serialized_dbus_msg)
        return msg
    except IndexError:
        # Occurs when Pickle can't parse the message.
        #print 'pickle: oops'
        pass
    return None
