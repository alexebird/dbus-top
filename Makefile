test:
	PYTHONPATH=. python tests/test_dbus_message.py

killdbm:
	killall dbus-monitor

.PHONY: test killall-dbus-monitors
