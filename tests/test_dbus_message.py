import unittest, sys

sys.path.insert(0, '.')
from dbustop import dbus_message

class TestDbusMessage(unittest.TestCase):
    def test_parse_signal(self):
        message_str = 'sig\t1279224860\t619607\t7\t/org/freedesktop/DBus\torg.freedesktop.DBus\tNameOwnerChanged\n'
        parsed_message = dbus_message.parse(message_str)
        self.assertNotEqual(parsed_message, None)
        self.assertEqual(parsed_message.message_type, 'sig')
        self.assertEqual(parsed_message.timestamp, 1279224860 + (619607 / 1000000.0))
        self.assertEqual(parsed_message.serial, 7)
        self.assertEqual(parsed_message.object, '/org/freedesktop/DBus')
        self.assertEqual(parsed_message.interface, 'org.freedesktop.DBus')
        self.assertEqual(parsed_message.member, 'NameOwnerChanged')
        
    def test_parse_method_call(self):
        message_str = 'mc\t1279224860\t619617\t2\t:1.12390\t/SomeObject\tcom.example.SampleInterface\tHelloWorld\n'
        parsed_message = dbus_message.parse(message_str)
        self.assertNotEqual(parsed_message, None)
        self.assertEqual(parsed_message.message_type, 'mc')
        self.assertEqual(parsed_message.timestamp, 1279224860 + (619617 / 1000000.0))
        self.assertEqual(parsed_message.sender, ':1.12390')
        self.assertEqual(parsed_message.serial, 2)
        self.assertEqual(parsed_message.object, '/SomeObject')
        self.assertEqual(parsed_message.interface, 'com.example.SampleInterface')
        self.assertEqual(parsed_message.member, 'HelloWorld')

    def test_parse_method_return(self):
        message_str = 'mr\t1279224860\t619619\t44\t2\t:1.12390\n'
        parsed_message = dbus_message.parse(message_str)
        self.assertNotEqual(parsed_message, None)
        self.assertEqual(parsed_message.message_type, 'mr')
        self.assertEqual(parsed_message.timestamp, 1279224860 + (619619 / 1000000.0))
        self.assertEqual(parsed_message.serial, 44)
        self.assertEqual(parsed_message.reply_serial, 2)
        self.assertEqual(parsed_message.destination, ':1.12390')

    def test_parse_error(self):
        message_str = 'err\t1279225677\t616434\t105\t2\t:1.12454\n'
        parsed_message = dbus_message.parse(message_str)
        self.assertNotEqual(parsed_message, None)
        self.assertEqual(parsed_message.message_type, 'err')
        self.assertEqual(parsed_message.timestamp, 1279225677 + (616434 / 1000000.0))
        self.assertEqual(parsed_message.serial, 105)
        self.assertEqual(parsed_message.reply_serial, 2)
        self.assertEqual(parsed_message.destination, ':1.12454')

if __name__ == '__main__':
    unittest.main()
