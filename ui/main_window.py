from PyQt5.QtWidgets import QLabel, QSlider, QWidget
from PyQt5.QtCore import Qt

from controllers.brightness_control import BrightnessController


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.brightness_controller = BrightnessController()
        self.sliderValues = []
        self.create_sliders(len(self.brightness_controller.monitors))

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)
        self.setObjectName("MainWindow")

        self.setStyleSheet(self.create_stylesheet())
        self.setAttribute(Qt.WA_StyledBackground)

    def create_sliders(self, num_sliders=1):
        sliders = []

        for i in range(num_sliders):
            label = QLabel(self, text=f"Monitor {i+1}:")
            label.move(10, i*60 + 10)

            slider = QSlider(self, orientation=Qt.Horizontal)

            self.set_position(slider, i)
            self.configure_brightness_controll(slider, monitor=i)

            sliders.append(slider)

        return sliders

    def set_position(self, slider, i):
        slider.setRange(0, 100)

        slider.move(10, i*60 + 30)

        slider.setMaximumSize(300, 40)
        slider.setMinimumSize(200, 30)

    def configure_brightness_controll(self, slider: QSlider, monitor):
        initial_brightness = self.brightness_controller.get_current_brightness(monitor)
        slider.setValue(initial_brightness[0])
        self.sliderValues.append(initial_brightness[0])

        slider.valueChanged.connect(lambda value, monitor=monitor: self.sliderValues.__setitem__(monitor, value))
        slider.sliderReleased.connect(lambda monitor=monitor: self.brightness_controller.set_brightness(self.sliderValues[monitor], monitor))

    def update_brightness(self, monitor):
        self.brightness_controller.set_brightness(self.sliderValues[monitor], monitor)

    def create_stylesheet(self):
        return """
                QWidget#MainWindow {
                    background-color: #333;
                    color: #fff;
                    border: 1px solid #555;
                }
                
                QLabel {
                    color: #ddd;
                }
                """
