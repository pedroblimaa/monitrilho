from PyQt5.QtWidgets import QLabel, QSlider, QWidget, QProxyStyle
from PyQt5.QtCore import Qt

from controllers.brightness_control import BrightnessController


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.is_pressed = False

        self.brightness_controller = BrightnessController()
        self.slider_values = []
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
            slider.setStyle(ProxyStyle())

            self.set_slider_position(slider, i)
            self.configure_brightness_control(slider, monitor=i)

            sliders.append(slider)

        return sliders

    def set_slider_position(self, slider, i):
        slider.setRange(0, 100)

        slider.move(10, i*60 + 30)

        slider.setMaximumSize(300, 40)
        slider.setMinimumSize(200, 30)

    def configure_brightness_control(self, slider: QSlider, monitor):
        initial_brightness = self.brightness_controller.get_current_brightness(monitor)
        slider.setValue(initial_brightness[0])
        self.slider_values.append(initial_brightness[0])

        slider.valueChanged.connect(
            lambda value, monitor=monitor: self.update_brightness_when_value_changes(value, monitor)
        )
        slider.sliderReleased.connect(
            lambda monitor=monitor: self.update_brightness_when_released(monitor)
        )
        slider.sliderPressed.connect(lambda: self.update_pressed_flag(True))

    def update_brightness_when_value_changes(self, value, monitor):
        self.slider_values[monitor] = value
        if not self.is_pressed:
            self.brightness_controller.set_brightness(self.slider_values[monitor], monitor)

    def update_brightness_when_released(self, monitor):
        self.update_pressed_flag(False)
        self.brightness_controller.set_brightness(self.slider_values[monitor], monitor)

    def update_pressed_flag(self, is_pressed):
        self.is_pressed = is_pressed

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


class ProxyStyle(QProxyStyle):
    def style_hint(self, hint, opt=None, widget=None, return_data=None):
        res = super().style_hint(hint, opt, widget, returnData=return_data)

        if hint == self.SH_Slider_AbsoluteSetButtons:
            res |= Qt.LeftButton

        return res
