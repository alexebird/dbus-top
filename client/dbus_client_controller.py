class DbusClientController:
    def __init__(self):
        self.ui_thread = None
        self.network_thread = None

    def dbus_message_received(self, message):
        self.ui_thread.print_str('message')

    def key_pressed(self, character):
        print 'key_pressed',
        self.ui_thread.print_str(character)
        if character == 'q':
            print 'calling stop',
            self.ui_thread.refresh()
            self.network_thread.stop()
            self.ui_thread.stop()
