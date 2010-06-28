import shlex
import struct
import re
import pickle

class DbusMessage:
    packet_length_format = '!i'

    def __init__(self, first_line):
        self.raw_lines = []
        self.add_line(first_line)

    def add_line(self, line):
        self.raw_lines.append(line)

    def to_string(self):
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

    #
    # Serialize the DbusMessage to be sent over a network stream using pickle, but
    # prepend the length of the pickle dump.  Returns the length as an int byte string
    # form plus the pickle dump string itself.
    #
    def packetize(self):
        data = pickle.dumps(self)
        length_bytes = struct.pack(DbusMessage.packet_length_format, len(data))
        return length_bytes + data

    def parse(self):
        header_line = self.raw_lines[0]
        body = '\n'.join(self.raw_lines[1:-1])
        tokens = shlex.split(header_line)
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
        self.raw_lines = None
        #self.body = body
        #for k,v in nonterms.iteritems():
            #print '%-15s => %s' % (k, v)

def unpack_packet_length(length_in_bytes):
    # unpack() always returns a tuple.
    return struct.unpack(DbusMessage.packet_length_format, length_in_bytes)[0]
        
