import cv2
import numpy as np

from src.SharedPackage import ScreenRegion, Constants, Coordinate
from src.VendorPackage import PyAutoGui, Cv2File
from src.OperatingSystemPackage import Monitor
from src.LoggerPackage import Logger


class GlobalGameWidgetContainer:
    def __init__(self, monitor: Monitor, pyautogui: PyAutoGui, initial_floor_lvl: int):
        self.__monitor = monitor
        self.__initial_setup_screenshot = monitor.screenshot()
        self.__monitor_dimensions = monitor.specifications()

        Logger.info('Locating BattleList...')
        self.__battle_list_widget_region = pyautogui.locate_battle_list_widget(
            self.__initial_setup_screenshot,
            self.__monitor_dimensions
        )

        Logger.info('Locating Health...')
        self.__health_widget_region = pyautogui.locate_health_widget(
            self.__initial_setup_screenshot,
            self.__monitor_dimensions
        )

        Logger.info('Locating Mana...')
        self.__mana_widget_region = pyautogui.locate_mana_widget(
            self.__initial_setup_screenshot,
            self.__monitor_dimensions
        )

        Logger.info('Locating Game Window...')
        self.__game_window = self.__locate_game_window_location()

        Logger.info('Creating Looting Area...')
        self.__looting_area_coordinates = self.__create_looting_area_coordinates()

        Logger.info('Locating MiniMap...')
        self.__mini_map_widget_region = self.__locate_mini_map_widget()

        Logger.info('Locating Floor Widget...')
        self.__floor_widget_region = self.__locate_floor_widget(initial_floor_lvl)

        Logger.info('Locating Combat Stance Widget...')
        self.__combat_stance_region = self.__locate_combat_stance_widget()

        Logger.info('Locating Ring Widget...')
        self.__ring_region = self.__locate_ring_widget()

        Logger.info('Locating Nearest Depot...')
        self.__nearest_depot_region = self.__locate_depot()

    def battle_list_widget(self) -> ScreenRegion:
        return self.__battle_list_widget_region

    def health_widget(self) -> ScreenRegion:
        return self.__health_widget_region

    def mana_widget(self) -> ScreenRegion:
        return self.__mana_widget_region

    def game_window(self) -> ScreenRegion:
        return self.__game_window

    def mini_map_widget(self) -> ScreenRegion:
        return self.__mini_map_widget_region

    def floor_level_widget(self) -> ScreenRegion:
        return self.__floor_widget_region

    def looting_area(self) -> list[Coordinate]:
        return self.__looting_area_coordinates

    def combat_stance_widget(self) -> ScreenRegion:
        return self.__combat_stance_region

    def ring_widget(self) -> ScreenRegion:
        return self.__ring_region

    def nearest_depot(self) -> ScreenRegion:
        return self.__nearest_depot_region

    def __create_looting_area_coordinates(self,) -> list[Coordinate]:
        [width, _] = self.__monitor_dimensions

        pixels = int((width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_PLAYER_TO_LOOT_PIXELS)

        center_game_window_coordinate = Coordinate.from_screen_region(self.__game_window)

        first_looting_point = Coordinate(center_game_window_coordinate.x, center_game_window_coordinate.y - pixels)
        second_looting_point = Coordinate(center_game_window_coordinate.x + pixels, first_looting_point.y)
        third_looting_point = Coordinate(center_game_window_coordinate.x + pixels, center_game_window_coordinate.y)
        fourth_looting_point = Coordinate(third_looting_point.x, third_looting_point.y + pixels)
        fifth_looting_point = Coordinate(center_game_window_coordinate.x, center_game_window_coordinate.y + pixels)
        six_looting_point = Coordinate(center_game_window_coordinate.x - pixels, fifth_looting_point.y)
        seven_looting_point = Coordinate(center_game_window_coordinate.x - pixels, center_game_window_coordinate.y)
        eight_looting_point = Coordinate(seven_looting_point.x, center_game_window_coordinate.y - pixels)

        return list([
            first_looting_point,
            second_looting_point,
            third_looting_point,
            fourth_looting_point,
            fifth_looting_point,
            six_looting_point,
            seven_looting_point,
            eight_looting_point
        ])

    def __locate_game_window_location(self,) -> ScreenRegion:
        frame = cv2.cvtColor(self.__initial_setup_screenshot, cv2.COLOR_BGR2GRAY)

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

        [width, _] = self.__monitor_dimensions

        start_number = int(
            (width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_GAME_WIDGET_X_ANCHOR_TO_START_NUMBER)
        end_number = int(
            (width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_GAME_WIDGET_X_ANCHOR_TO_END_NUMBER)

        start_x = left_arrow_start_x + start_number
        end_x = right_arrow_start_x - end_number
        start_y = left_arrow_start_y + left_arrow_height
        end_y = int((width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_GAME_WIDGET_Y_ANCHOR_TO_END_NUMBER)

        return ScreenRegion(start_x, end_x, start_y, end_y)

    def __locate_mini_map_widget(self) -> ScreenRegion:
        frame = cv2.cvtColor(self.__initial_setup_screenshot, cv2.COLOR_BGR2GRAY)

        mini_map_anchor = Cv2File.load_image('src/Wiki/Ui/Map/radar_anchor.png')

        match = cv2.matchTemplate(frame, mini_map_anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        start_x = x - self.__monitor.adjust_pixel_to_monitor(Constants.REFERENCE_MINI_MAP_START_X)
        end_x = start_x + self.__monitor.adjust_pixel_to_monitor(Constants.REFERENCE_MINI_MAP_END_X)
        start_y = y - self.__monitor.adjust_pixel_to_monitor(Constants.REFERENCE_MINI_MAP_START_Y)
        end_y = start_y + self.__monitor.adjust_pixel_to_monitor(Constants.REFERENCE_MINI_MAP_END_Y)

        return ScreenRegion(start_x, end_x, start_y, end_y)

    def __locate_floor_widget(self, initial_floor_lvl: int) -> ScreenRegion:
        frame = cv2.cvtColor(self.__initial_setup_screenshot, cv2.COLOR_BGR2GRAY)

        floor_widget_anchor = Cv2File.load_image(f'src/Wiki/Ui/Map/FloorLevel/{initial_floor_lvl}.png')

        match = cv2.matchTemplate(frame, floor_widget_anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        height, width = floor_widget_anchor.shape

        start_y = y
        end_y = y + height
        start_x = x
        end_x = x + width

        return ScreenRegion(start_x, end_x, start_y, end_y)

    def __locate_combat_stance_widget(self) -> ScreenRegion:
        frame = cv2.cvtColor(self.__initial_setup_screenshot, cv2.COLOR_BGR2GRAY)

        combat_stance_anchor = Cv2File.load_image(f'src/Wiki/Ui/Battle/combat_stance.png')

        match = cv2.matchTemplate(frame, combat_stance_anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        height, width = combat_stance_anchor.shape

        start_y = y
        end_y = y + height
        start_x = x
        end_x = x + width

        return ScreenRegion(start_x, end_x, start_y, end_y)

    def __locate_ring_widget(self) -> ScreenRegion:
        frame = cv2.cvtColor(self.__initial_setup_screenshot, cv2.COLOR_BGR2GRAY)

        ring_anchor = Cv2File.load_image(f'src/Wiki/Ui/Battle/ring_anchor.png')

        match = cv2.matchTemplate(frame, ring_anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        height, width = ring_anchor.shape

        start_y = y
        end_y = y + height
        start_x = x
        end_x = x + width

        return ScreenRegion(start_x, end_x, start_y, end_y)
    def __locate_depot(self) -> ScreenRegion:
        frame = cv2.cvtColor(self.__initial_setup_screenshot, cv2.COLOR_BGR2GRAY)

        depot_anchor = Cv2File.load_image(f'src/Wiki/Ui/Market/depot.png')

        match = cv2.matchTemplate(depot_anchor, frame, cv2.TM_CCOEFF_NORMED)

        multiple_loc = np.where(match >= 0.9)

        depot_locations = []

        for pt in zip(*multiple_loc[::-1]):
            depot_locations.append(pt)

        screen_player_position = Coordinate.from_screen_region(self.__game_window)

        distances = []
        for depot_loc in depot_locations:
            distance = np.linalg.norm(np.array(screen_player_position) - np.array(depot_loc))
            distances.append(distance)

        # Find the index of the nearest depot
        nearest_depot_index = np.argmin(distances)

        # Get the coordinates of the nearest depot
        nearest_depot_loc = depot_locations[nearest_depot_index]

        height, width = depot_anchor.shape

        print(nearest_depot_loc)

        return ScreenRegion(
            start_x=0,
            end_x=0 + width,
            start_y=0,
            end_y=0 + height
        )
