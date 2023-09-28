import os
import sys
import atexit
from PyQt5.QtWidgets import QMessageBox


class InstanceManager():
    def __init__(self):
        super().__init__()

        self.lock_file_path = os.path.join(os.path.expanduser("~"), ".monitrilho_lock")
        self.check_single_instance()

    def check_single_instance(self):
        if os.path.exists(self.lock_file_path):
            self.show_alert("Another instance is already running.")
            sys.exit(1)
        else:
            with open(self.lock_file_path, "w") as lock_file:
                lock_file.write(str(os.getpid()))

        atexit.register(self.remove_lock_file)

    def show_alert(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

    def remove_lock_file(self):
        os.remove(self.lock_file_path)
