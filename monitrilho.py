import sys
import threading
from PyQt5.QtWidgets import QApplication
from ui.instance_manager import InstanceManager
from ui.system_tray_icon import SystemTrayIcon


def listen_for_signal(instance_manager: InstanceManager, system_tray_icon: SystemTrayIcon):
    listener_thread = threading.Thread(
        target=instance_manager.listen_for_signal,
        args=(system_tray_icon.show_main_window,)
    )
    listener_thread.start()


if __name__ == '__main__':
    app = QApplication([])
    instanceManager = InstanceManager()

    app.setQuitOnLastWindowClosed(False)

    system_tray_icon = SystemTrayIcon(instance_manager=instanceManager)
    system_tray_icon.show()

    listen_for_signal(instanceManager, system_tray_icon)

    sys.exit(app.exec_())
