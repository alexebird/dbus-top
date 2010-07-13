print 'IMPORTING:', __name__
import sys
for m in sys.modules: print m
import base_thread
for m in sys.modules: print m
import dbus_message
import event

#from base_thread import BaseThread
#from dbus_message import DbusMessage
