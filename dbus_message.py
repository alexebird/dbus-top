import shlex
import re

class DbusMessage:
    def __init__(self, first_line):
        self.lines = []
        self.add_line(first_line)

    def add_line(self, line):
        self.lines.append(line)

    def print_msg(self):
        print '\n'.join(self.lines)

    def parse(self):
        first_line = self.lines[0]
        body = self.lines[1:-1]
        tokens = shlex.split(first_line)
        print first_line
        #print tokens

        key_value_re = re.compile('\S+=[^=\s]+')
        arrow_re = re.compile('->')

        curr_nonterm = ''
        nonterms = {}
        for t in tokens:
            if key_value_re.match(t):
                if curr_nonterm != '':
                    #key, value = curr_nonterm.strip().split('=', 1)
                    header_entity = curr_nonterm.strip().split('=', 1)
                    #print key, value
                    if len(nonterms) == 0:
                        nonterms['message_type'] = header_entity
                    else:
                        nonterms[header_entity[0]] = header_entity[1]
                curr_nonterm = t
            elif arrow_re.match(t):
                pass
            else:
                # algo won't work if there is a word without a '=' as the last word in the string
                curr_nonterm += ' ' + t
                #if t == tokens[-1]:
                    #nonterms.append(curr_nonterm.strip())

        for k,v in nonterms.iteritems():
            print '%-15s => %s' % (k, v)

