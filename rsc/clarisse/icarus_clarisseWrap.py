from PySide import QtCore, QtGui
import ix


class clarisseWrap:
    # Application helper
    def __init__(self, app):
        self.app = app
        self.timer = QtCore.QTimer()
        self.timer.start(1)
        # call clarisse application event loop
        self.timer.timeout.connect(self.process_clarisse_events)
        self.app.aboutToQuit.connect(self.kill_timer)

    def run(self):
        # we make sure to enable history as by default history is disabled in scripts.
        # remember the application will be running in the background
        # we want command history to be enabled!
        is_history_enabled = ix.application.get_command_manager().is_history_enabled()
        if not is_history_enabled:
            ix.enable_command_history()
        self.app.exec_()
        if not is_history_enabled:
            ix.disable_command_history()

    def kill_timer(self):
        self.timer.stop()

    def process_clarisse_events(self):
        # call clarisse application event loop and process callbacks
        ix.application.check_for_events()
							
def exec_(app):
    happ = clarisseWrap(app)
    happ.run()