class DbusMessage:
    def __init__(self, first_line):
        self.lines = []
        self.add_line(first_line)

    def add_line(self, line):
        self.lines.append(line)

    def print_msg(self):
        print '\n'.join(self.lines)

    def parse(self):
        pass
        # do some parsing
