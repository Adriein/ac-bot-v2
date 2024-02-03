from collections import ChainMap

import numpy as np
import cv2
import math

from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.VendorPackage import Cv2File
from src.SharedPackage import Waypoint, Coordinate

from .MapTile import MapTile
from .Script import Script


class Map:
    FALSE_NON_WALKABLE_POSITIVES = [
        "32439, 32308, 8",
        "32435, 32295, 8",
        "32423, 32303, 8",
        "32429, 32306, 8",
        "32430, 32302, 8",
        "32444, 32295, 9",
        "32444, 32294, 9",
        "32444, 32293, 9",
        "32883, 32066, 9",
        "32828, 32107, 9",
        "32828, 32107, 9",
        "32917 ,32187, 8",
        "32933, 32173, 9",
        "32894, 31905, 8",
        "32822, 31933, 6",
        "32828, 31927, 6",
        "32845, 31922, 6",
    ]

    def __init__(self, widget: GlobalGameWidgetContainer, script: Script):
        self.__widget = widget

        self.IGNORE_WAYPOINTS = self.FALSE_NON_WALKABLE_POSITIVES
        self.IN_MEMORY_FLOOR_PNG_MAP = ChainMap()

        for floor in script.floors():
            self.IN_MEMORY_FLOOR_PNG_MAP.setdefault(
                floor,
                Cv2File.load_image(f'src/Wiki/Ui/Map/Floors/floor-{floor}.png')
            )

    def where_am_i(self, frame: np.ndarray, last_known_waypoint: Waypoint, current_floor: int) -> MapTile:
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tibia_map = self.IN_MEMORY_FLOOR_PNG_MAP.get(current_floor)

        # find position of minimap in the screen
        mini_map_screen_region = self.__widget.mini_map_widget()

        start_y = mini_map_screen_region.start_y
        end_y = mini_map_screen_region.end_y
        start_x = mini_map_screen_region.start_x
        end_x = mini_map_screen_region.end_x

        mini_map_frame = grey_scale_frame[start_y:end_y, start_x:end_x]

        height, width = mini_map_frame.shape

        # cut a portion of the map based on last waypoint
        pixel_on_map = self.__get_map_coordinate_from_last_visited_waypoint(last_known_waypoint)

        map_start_x = pixel_on_map.x - (math.floor(width / 2) + 20)
        map_end_x = pixel_on_map.x + (math.floor(width / 2) + 20)

        map_start_y = pixel_on_map.y - (math.floor(height / 2) + 20)
        map_end_y = pixel_on_map.y + (math.floor(height / 2) + 1 + 20)

        tibia_map_roi = tibia_map[map_start_y:map_end_y, map_start_x:map_end_x]

        # find on this map portion the minimap
        match = cv2.matchTemplate(tibia_map_roi, mini_map_frame, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        start_x = pixel_on_map.x - 20 + x
        start_y = pixel_on_map.y - 20 + y

        return MapTile.from_pixel(Coordinate(start_x, start_y), current_floor)

    def which_floor_am_i(self, frame: np.array) -> int:
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        mini_map_screen_region = self.__widget.mini_map_widget()

        width = mini_map_screen_region.start_x - mini_map_screen_region.end_x

        left = mini_map_screen_region.start_x + width + 8
        top = mini_map_screen_region.start_y - 7
        height = 67
        width = 2

        actual_floor_lvl = grey_scale_frame[top:top + height, left:left + width]

        return 8

    def __get_map_coordinate_from_last_visited_waypoint(self, waypoint: Waypoint) -> Coordinate:
        return Coordinate(waypoint.x - 31744, waypoint.y - 30976)
