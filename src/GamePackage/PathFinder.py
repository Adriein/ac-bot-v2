import heapq

from .Map import Map
from .MapTile import MapTile

from src.UtilPackage import LinkedList
from src.SharedPackage import Waypoint


class PathFinder:
    def __init__(self, map: Map):
        self.__map = map

    def execute(self, current: Waypoint, destination: Waypoint, floor: int) -> LinkedList:
        path = LinkedList()

        tile_path = self.__a_star_algorithm(current, destination)

        if tile_path is None:
            return path

        for index, current_tile in enumerate(tile_path):
            try:
                destination_tile = tile_path[index + 1]

                direction = self.__waypoints_to_cardinal_direction(current_tile, destination_tile)
                path.append(MoveCommand(1, direction))
            except IndexError:
                pass

        return path

    def __a_star_algorithm(self, current: Waypoint, destination: Waypoint):
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

        for waypoint in self.__FALSE_POSITIVES:
            if waypoint == current.waypoint:
                return False

        pixel = self.__get_pixel_from_waypoint(current.waypoint)

        pixel_color = None

        if current.waypoint.z == 5:
            pixel_color = self.tibia_walkable_map_hsv_floor_5[pixel.y, pixel.x]

        if current.waypoint.z == 6:
            pixel_color = self.tibia_walkable_map_hsv_floor_6[pixel.y, pixel.x]

        if current.waypoint.z == 7:
            pixel_color = self.tibia_walkable_map_hsv_floor_7[pixel.y, pixel.x]

        if current.waypoint.z == 8:
            pixel_color = self.tibia_walkable_map_hsv_floor_8[pixel.y, pixel.x]

        if current.waypoint.z == 9:
            pixel_color = self.tibia_walkable_map_hsv_floor_9[pixel.y, pixel.x]

        if current.waypoint.z == 10:
            pixel_color = self.tibia_walkable_map_hsv_floor_10[pixel.y, pixel.x]

        mask = cv2.inRange(pixel_color, lower_yellow, upper_yellow)

        return np.all(mask == 255)
