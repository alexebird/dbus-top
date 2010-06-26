class DbusClientController:
    def __init__(self):
        self.message_q = []

    def dbus_message_received(self, message):
        #print message.to_string()
        self.message_q.append(message)
        self.ui_thread.refresh()

    def key_pressed(self, character):
        if character == 'q':
            self.shutdown_application()

    def shutdown_application(self):
        self.network_thread.stop()
        self.ui_thread.stop()
