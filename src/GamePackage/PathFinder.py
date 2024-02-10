import heapq

import numpy as np
import cv2

from .MapTile import MapTile

from src.UtilPackage import LinkedList, MapCollection
from src.SharedPackage import Waypoint, MoveCommand
from src.GamePackage import Script
from src.VendorPackage import Cv2File


class PathFinder:
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

    def __init__(self, script: Script):
        self.RESOLVED_PATHS_CACHE = MapCollection()
        self.IN_MEMORY_FLOOR_PATH_PNG_MAP = MapCollection()

        for floor in script.floors():
            map_path_screenshot = Cv2File.load_image(
                f'src/Wiki/Ui/Map/Walkable/floor-{floor}-path.png',
                False
            )

            map_path_screenshot_hsv = cv2.cvtColor(map_path_screenshot, cv2.COLOR_BGR2HSV)

            self.IN_MEMORY_FLOOR_PATH_PNG_MAP.set(
                floor,
                map_path_screenshot_hsv
            )

    def execute(self, current: Waypoint, destination: Waypoint) -> LinkedList[MoveCommand]:
        hashed_route = self.__hash_waypoint_set(current, destination)

        if self.RESOLVED_PATHS_CACHE.has(hashed_route):
            return self.RESOLVED_PATHS_CACHE.get(hashed_route)

        path = LinkedList()

        tile_path = self.__a_star_algorithm(current, destination)

        if not tile_path:
            return path

        for index, current_tile in enumerate(tile_path):
            try:
                destination_tile = tile_path[index + 1]

                direction = current_tile.waypoint.cardinal_direction_between_waypoints(destination_tile.waypoint)

                path.append(MoveCommand(1, direction))
            except IndexError:
                pass

        self.RESOLVED_PATHS_CACHE.set(hashed_route, path)

        return path

    def __a_star_algorithm(self, current: Waypoint, destination: Waypoint) -> list[MapTile]:
        open_set = []
        visited = set()

        start_map_tile = MapTile.build(current)
        start_map_tile.calculate_cost(current, destination)

        destination_map_tile = MapTile.build(destination)

        heapq.heappush(open_set, start_map_tile)

        while open_set:
            current_map_tile: MapTile = heapq.heappop(open_set)

            if current_map_tile == destination_map_tile:
                path = list()

                while current_map_tile:
                    path.append(current_map_tile)
                    current_map_tile = current_map_tile.parent

                path.reverse()

                return path

            visited.add(current_map_tile)

            current_map_tile.create_adjacent_tiles()

            for neighbor_map_tile in current_map_tile.adjacent_tiles:
                if neighbor_map_tile in visited:
                    continue

                if self.__is_not_walkable_waypoint(neighbor_map_tile):
                    visited.add(neighbor_map_tile)
                    continue

                neighbor_map_tile.calculate_cost(current, destination)

                if neighbor_map_tile.f_score < current_map_tile.f_score or neighbor_map_tile not in open_set:
                    neighbor_map_tile.parent = current_map_tile

                    if neighbor_map_tile not in open_set:
                        open_set.append(neighbor_map_tile)

    def __is_not_walkable_waypoint(self, current: MapTile) -> bool:
        # Define the lower and upper bounds of the yellow color range in BGR format
        lower_yellow = np.array([0, 100, 100], dtype=np.uint8)
        upper_yellow = np.array([100, 255, 255], dtype=np.uint8)

        for waypoint in self.FALSE_NON_WALKABLE_POSITIVES:
            if waypoint == current.waypoint:
                return False

        pixel = current.waypoint.to_coordinate()

        map_path_screenshot_hsv = self.IN_MEMORY_FLOOR_PATH_PNG_MAP.get(current.waypoint.z)

        pixel_color = map_path_screenshot_hsv[pixel.y, pixel.x]

        mask = cv2.inRange(pixel_color, lower_yellow, upper_yellow)

        return np.all(mask == 255)

    def __hash_waypoint_set(self, current: Waypoint, destination: Waypoint) -> str:
        return f'{current.hash()}{destination.hash()}'
