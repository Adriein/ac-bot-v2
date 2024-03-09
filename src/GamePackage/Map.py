import numpy as np
import cv2
import math
import hashlib

from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.VendorPackage import Cv2File, PyAutoGui
from src.SharedPackage import Waypoint, Coordinate, MoveCommand
from src.UtilPackage import MapCollection

from .MapTile import MapTile
from .Script import Script
from .PathFinder import PathFinder


class Map:
    def __init__(self, widget: GlobalGameWidgetContainer, script: Script, path_finder: PathFinder):
        self.__widget = widget
        self.__path_finder = path_finder

        self.IN_MEMORY_FLOOR_PNG_MAP = MapCollection()
        self.IN_MEMORY_FLOOR_LVL_MAP = MapCollection()

        for floor in script.floors():
            print(floor)
            self.IN_MEMORY_FLOOR_PNG_MAP.set(
                floor,
                Cv2File.load_image(f'src/Wiki/Ui/Map/Floors/floor-{floor}.png')
            )

            color_floor_lvl_image = Cv2File.load_image(f'src/Wiki/Ui/Map/FloorLevel/{floor}.png', False)
            floor_lvl_image = cv2.cvtColor(color_floor_lvl_image, cv2.COLOR_BGR2GRAY)

            image_hash = hashlib.sha256(floor_lvl_image.tobytes()).hexdigest()

            self.IN_MEMORY_FLOOR_LVL_MAP.set(
                image_hash,
                floor
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
        pixel_on_map = last_known_waypoint.to_coordinate()

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

        floor_lvl_widget = self.__widget.floor_level_widget()

        start_y = floor_lvl_widget.start_y
        end_y = floor_lvl_widget.end_y
        start_x = floor_lvl_widget.start_x
        end_x = floor_lvl_widget.end_x

        actual_floor_lvl = grey_scale_frame[start_y:end_y, start_x:end_x]

        image_hash = hashlib.sha256(actual_floor_lvl.tobytes()).hexdigest()

        return self.IN_MEMORY_FLOOR_LVL_MAP.get(image_hash)

    def find_shortest_path(self, current: Waypoint, destination: Waypoint) -> list[MoveCommand]:
        return self.__path_finder.execute(current, destination)
