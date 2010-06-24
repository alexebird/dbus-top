import shlex
import re
import pickle

class DbusMessage:
    def __init__(self, first_line):
        self.raw_lines = []
        self.add_line(first_line)

    def add_line(self, line):
        self.raw_lines.append(line)

    def print_msg(self):
        print 'dbus-message: %s...' % self.raw_lines[0][0:40]

    def serialize(self):
        return pickle.dumps(self.header)

    def parse(self):
        header_line = self.raw_lines[0]
        body = '\n'.join(self.raw_lines[1:-1])
        tokens = shlex.split(header_line)
        key_value_re = re.compile('\S+=[^=\s]+')
        arrow_re = re.compile('->')
        curr_header_entry = ''
        header_entries = {}
        #import pdb; pdb.set_trace()
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
        self.body = body
        self.header = header_entries
        #for k,v in nonterms.iteritems():
            #print '%-15s => %s' % (k, v)
