from src.SharedPackage import ScreenRegion
from src.VendorPackage import PyAutoGui
from src.OperatingSystemPackage import Monitor
from src.LoggerPackage import Logger


class GlobalGameWidgetContainer:
    def __init__(self, monitor: Monitor, pyautogui: PyAutoGui):
        initial_setup_screenshot = monitor.screenshot()
        monitor_dimensions = monitor.specifications()

        Logger.info('Locating BattleList...')
        self.__battle_list_widget_region = pyautogui.locate_battle_list_widget(
            initial_setup_screenshot,
            monitor_dimensions
        )

        Logger.info('Locating Health...')
        self.__health_widget_region = pyautogui.locate_health_widget(
            initial_setup_screenshot,
            monitor_dimensions
        )

        Logger.info('Locating Mana...')
        self.__mana_widget_region = pyautogui.locate_mana_widget(
            initial_setup_screenshot,
            monitor_dimensions
        )

    def battle_list_widget(self) -> ScreenRegion:
        return self.__battle_list_widget_region

    def health_widget(self) -> ScreenRegion:
        return self.__health_widget_region

    def mana_widget(self) -> ScreenRegion:
        return self.__mana_widget_region
