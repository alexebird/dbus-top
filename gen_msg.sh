#!/bin/bash
while true; do 
	dbus-send --dest='org.freedesktop.DBus' /org/freedesktop/DBus org.freedesktop.DBus.Peer.Ping
	sleep 1
done
