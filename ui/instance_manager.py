import os
import sys
import atexit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QLockFile  # import QLockFile class


LOCK_FILE_PATH = os.path.join(os.path.expanduser("~"), "monitrilho.lock")


class InstanceManager():
    def __init__(self):
        super().__init__()
        self.check_single_instance()

    def check_single_instance(self):
        self.lock_file = QLockFile(LOCK_FILE_PATH)  # create a lock file object

        if not self.lock_file.tryLock():  # try to lock the file
            self.show_alert("Another instance is already running.")
            sys.exit(1)

    def show_alert(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()