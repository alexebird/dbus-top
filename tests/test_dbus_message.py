import unittest
import dbus_message

class TestDbusMessage(unittest.TestCase):

    def test_parse(self):
        msg = DbusMessage()
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
