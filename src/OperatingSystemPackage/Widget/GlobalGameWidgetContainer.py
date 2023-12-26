from src.SharedPackage import ScreenRegion
from src.VendorPackage import PyAutoGui
from src.OperatingSystemPackage import Monitor


class GlobalGameWidgetContainer:
    def __init__(self, monitor: Monitor, pyautogui: PyAutoGui):
        initial_setup_screenshot = monitor.screenshot()

        self.__battle_list_widget_region = pyautogui.locate_battle_list_widget(
            initial_setup_screenshot,
            monitor.specifications()
        )

    def battle_list_widget(self,) -> ScreenRegion:
        return self.__battle_list_widget_region
