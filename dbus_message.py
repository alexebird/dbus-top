import shlex
import re
import pickle

class DbusMessage:
    def __init__(self, first_line):
        self.lines = []
        self.message = None
        self.add_line(first_line)

    def add_line(self, line):
        self.lines.append(line)

    def print_msg(self):
        print '\n'.join(self.lines)

    def serialize(self):
        return pickle.dumps(self.message)

    def parse(self):
        first_line = self.lines[0]
        body = '\n'.join(self.lines[1:-1])
        tokens = shlex.split(first_line)
        #print 'line: ', first_line
        #print 'tokens: ', tokens
        key_value_re = re.compile('\S+=[^=\s]+')
        arrow_re = re.compile('->')
        curr_nonterm = ''
        nonterms = {}
        for t in tokens:
            if arrow_re.match(t):
                continue
            if key_value_re.match(t) == None:
                curr_nonterm += ' ' + t
                i = tokens.index(t)
                if key_value_re.match(tokens[i + 1]) or i + 1 >= len(tokens):
                    if len(nonterms) == 0:
                        nonterms['message_type'] = curr_nonterm.strip()
            else:
                curr_nonterm = t
                key, value = curr_nonterm.split('=', 1)
                nonterms[key.strip()] = value.strip()
        #nonterms['body'] = body
        self.message = nonterms
        #for k,v in nonterms.iteritems():
            #print '%-15s => %s' % (k, v)
