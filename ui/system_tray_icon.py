from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon
import darkdetect

from ui.main_window import MainWindow


class SystemTrayIcon(QSystemTrayIcon):
    
    def __init__(self, instance_manager):

        self.main_window = MainWindow()

        icon_path = 'assets\\light-ico.svg' if darkdetect.isDark() else 'assets\\dark-ico.svg'

        super().__init__(QIcon(icon_path), self.main_window)

        self.setToolTip("Your App Name")
        self.activated.connect(self.tray_icon_activated)

        self.tray_menu = QMenu(self.main_window)
        self.toggle_action = QAction("Toggle", self)
        self.toggle_action.triggered.connect(self.toggle_main_window)
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.exit_app)
        self.tray_menu.addAction(self.toggle_action)
        self.tray_menu.addAction(self.exit_action)
        self.setContextMenu(self.tray_menu)

        self.main_window_visible = False

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.toggle_main_window()

    def toggle_main_window(self):
        if self.main_window.isVisible():
            self.main_window.close()
        else:
            self.main_window.show()
            self.main_window.raise_()

            self.set_window_geometry()

    def set_window_geometry(self):
        tray_geometry = self.geometry()
        main_window_size = self.main_window.size()
        main_window_x = tray_geometry.bottomLeft().x() - main_window_size.width() - 10
        main_window_y = tray_geometry.bottom() - main_window_size.height() - 10

        self.main_window.setGeometry(
            main_window_x,
            main_window_y,
            main_window_size.width(),
            main_window_size.height()
        )

    def exit_app(self):
        QApplication.instance().quit()
