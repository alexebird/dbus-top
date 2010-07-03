import os

from dbustop.common.base_thread import BaseThread

class DbusMonitorMonitor(BaseThread):
    def __init__(self):
		BaseThread.__init__(self, 'DbusMonitorMonitor_thread')

    def run(self):
		fd_r, fd_w = os.pipe()

		if os.fork() == 0:
			# Child process: exec dbus-monitor and pipe output to parent
			os.close(fd_r)
			os.dup2(fd_w, sys.stdout.fileno())
			child_name = '/usr/bin/dbus-monitor'
			os.execl(child_name, child_name, '--session')
		else:
			# Parent process: Read from the dbus-monitor pipe and parse dbus messages.
			os.close(fd_w)
			dbm_file = os.fdopen(fd_r)

        while self.should_run():
			line = dbm_file.readline().rstrip()
			# Make sure the line doesn't start with spaces
			if re.match('^\S.*', line):
				msg = DbusMessage(line)
				# TODO add event to event queue
