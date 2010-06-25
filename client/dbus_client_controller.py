class DbusClientController:
    def __init__(self):
        self.ui_thread = None
        self.network_thread = None

    def dbus_message_received(self, message):
        self.ui_thread.print_str('message')
        #print message

    def key_pressed(self, character):
        self.ui_thread.print_str(character)
        if character == 'q':
            self.ui_thread.refresh()
            self.network_thread.stop()
            self.network_thread.shutdown_event.set()
            self.ui_thread.stop()
            self.ui_thread.shutdown_event.set()
