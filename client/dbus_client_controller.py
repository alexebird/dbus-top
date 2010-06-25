class DbusClientController:
    def __init__(self):
        self.message_q = []

    def dbus_message_received(self, message):
        self.message_q.append(message)
        #if len(self.message_q) > 25:
            #self.message_q.pop(0)
        self.ui_thread.refresh()

    def key_pressed(self, character):
        #self.ui_thread.print_str(character)
        if character == 'q':
            #self.ui_thread.refresh()
            self.shutdown_application()

    def shutdown_application(self):
        self.network_thread.stop()
        self.ui_thread.stop()
