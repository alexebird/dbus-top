test:
	python test/test_dbus_message.py

kill-dbus-monitors:
	killall dbus-monitor

.PHONY: test killall-dbus-monitors
