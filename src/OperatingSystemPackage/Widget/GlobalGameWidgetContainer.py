import numpy as np
import cv2

from src.SharedPackage import ScreenRegion, Constants
from src.VendorPackage import PyAutoGui, Cv2File
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

        Logger.info('Locating Game Window...')
        self.__game_window = self.__locate_game_window_location(initial_setup_screenshot, monitor_dimensions)

    def battle_list_widget(self) -> ScreenRegion:
        return self.__battle_list_widget_region

    def health_widget(self) -> ScreenRegion:
        return self.__health_widget_region

    def mana_widget(self) -> ScreenRegion:
        return self.__mana_widget_region

    def game_window(self) -> ScreenRegion:
        return self.__game_window

    def __locate_game_window_location(self, frame: np.ndarray, monitor_dimensions: tuple[int, int]) -> ScreenRegion:
        left_game_window_arrow = Cv2File.load_image(f'src/Wiki/Ui/GameWindow/left_game_window_arrow.png')
        right_game_window_arrow = Cv2File.load_image(f'src/Wiki/Ui/GameWindow/right_game_window_arrow.png')

        match = cv2.matchTemplate(frame, left_game_window_arrow, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        match = cv2.matchTemplate(frame, right_game_window_arrow, cv2.TM_CCOEFF_NORMED)

        (left_arrow_start_x, left_arrow_start_y) = max_coordinates

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (right_arrow_start_x, right_arrow_start_y) = max_coordinates

        left_arrow_height, left_arrow_width = left_game_window_arrow.shape
        _, right_arrow_width = right_game_window_arrow.shape

        [width, _] = monitor_dimensions

        start_number = int((width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_GAME_WIDGET_X_ANCHOR_TO_START_NUMBER)
        end_number = int((width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_GAME_WIDGET_X_ANCHOR_TO_END_NUMBER)

        start_x = left_arrow_start_x + start_number
        end_x = right_arrow_start_x - end_number
        start_y = left_arrow_start_y + left_arrow_height
        end_y = int((width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_GAME_WIDGET_Y_ANCHOR_TO_END_NUMBER)

        return ScreenRegion(start_x, end_x, start_y, end_y)
