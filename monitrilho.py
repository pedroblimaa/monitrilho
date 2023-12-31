import sys
from PyQt5.QtWidgets import QApplication
from ui.instance_manager import InstanceManager
from ui.system_tray_icon import SystemTrayIcon


if __name__ == '__main__':
    app = QApplication([])
    instanceManager = InstanceManager()

    app.setQuitOnLastWindowClosed(False)

    system_tray_icon = SystemTrayIcon()
    system_tray_icon.show()

    sys.exit(app.exec_())
