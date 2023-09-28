import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.instance_manager import InstanceManager
from ui.system_tray_icon import SystemTrayIcon


if __name__ == '__main__':
    try:
        app = QApplication([])
        instanceManager = InstanceManager()

        app.setQuitOnLastWindowClosed(False)

        system_tray_icon = SystemTrayIcon()
        system_tray_icon.show()

        sys.exit(app.exec_())
    except Exception as e:
        instanceManager.show_alert("Error starting application.")
        instanceManager.remove_lock_file()
        raise e
