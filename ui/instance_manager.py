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
        self.lock_file = QLockFile(self.lock_file_path)  # create a lock file object

        if not self.lock_file.tryLock():  # try to lock the file
            self.show_alert("Another instance is already running.")
            sys.exit(1)
        else:
            self.lock_file.unlock()  # unlock the file
            with open(self.lock_file_path, "w") as lock_file:
                lock_file.write(str(os.getpid()))  # write the PID to the file
            self.lock_file.lock()

        atexit.register(self.remove_lock_file)

    def show_alert(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

    def remove_lock_file(self):
        self.lock_file.unlock()
        os.remove(self.lock_file_path)  # remove the fil
