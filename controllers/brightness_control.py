from screen_brightness_control import set_brightness, list_monitors, get_brightness

class BrightnessController:
    def __init__(self):
        self.monitors = list_monitors()

    def get_current_brightness(self, display=0):
        return get_brightness(display)

    def set_brightness(self, display=0, value=100):
        set_brightness(display, value)

    def list_available_monitors(self):
        return list_monitors()
    