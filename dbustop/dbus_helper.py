import sys
import json

import dbus

def list_services(bus):
    print bus
    bus_class = dbus.SystemBus
    if bus == 'session':
        bus_class = dbus.SessionBus
    elif bus != 'system':
        return None

    bus = bus_class()
    listing = bus.list_names()
    listing.sort()
    return json.dumps(listing)
