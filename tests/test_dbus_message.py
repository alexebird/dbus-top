import unittest
from common.dbus_message import DbusMessage

class TestDbusMessage(unittest.TestCase):

    def test_parse_with_null_destination(self):
        header_line = 'signal sender=org.freedesktop.DBus -> dest=(null destination) serial=8 path=/org/freedesktop/DBus; interface=org.freedesktop.DBus; member=NameOwnerChanged'
        body_lines = ['   string ":1.1738"',
                      '   string ":1.1738"',
                      '   string ""']
        header = {'message_type': 'signal',
                  'sender': 'org.freedesktop.DBus',
                  'dest': '(null destination)',
                  'serial': '8',
                  'path': '/org/freedesktop/DBus;',
                  'interface': 'org.freedesktop.DBus;',
                  'member': 'NameOwnerChanged'}
        body = '   string ":1.1738"\n   string ":1.1738"\n   string ""\n'
        msg = DbusMessage(header_line)
        for l in body:
            msg.add_line(l)
        msg.parse()
        self.__compare_headers(header, msg.header)

    def test_parse_with_method_call(self):
        header_line = 'method call sender=:1.1776 -> dest=org.freedesktop.DBus serial=2 path=/org/freedesktop/DBus; interface=org.freedesktop.DBus; member=AddMatch'
        body_lines = ['   string "type=\'signal\'"']

        header = {'message_type': 'method call',
                'sender': ':1.1776',
                  'dest': 'org.freedesktop.DBus',
                  'serial': '2',
                  'path': '/org/freedesktop/DBus;',
                  'interface': 'org.freedesktop.DBus;',
                  'member': 'AddMatch'}
        body = '   string "type=\'signal\'"'
        msg = DbusMessage(header_line)
        for l in body:
            msg.add_line(l)
        msg.parse()
        self.__compare_headers(header, msg.header)

    def __compare_headers(self, h1, h2):
        for k,v in h1.items():
            self.assertEqual(h1[k], h2[k])

if __name__ == '__main__':
    unittest.main()
