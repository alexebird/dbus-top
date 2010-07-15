import unittest, sys

sys.path.insert(0, '.')
from dbustop import dbus_helper

class TestDbusMessage(unittest.TestCase):
    def test_parse_with_null_destination(self):
        services = dbus_helper.list_services('session')
        print services
        self.assertNotEqual(services, None)
        self.assertNotEqual(services, 'null')

if __name__ == '__main__':
    unittest.main()
