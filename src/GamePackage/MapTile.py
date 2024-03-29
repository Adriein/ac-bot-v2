import uuid

from src.SharedPackage import Coordinate, Waypoint


class MapTile:
    @staticmethod
    def from_pixel(coordinate: Coordinate, floor: int) -> 'MapTile':
        return MapTile(uuid.uuid4(), Waypoint(coordinate.x + 31744, coordinate.y + 30976, floor, Waypoint.UNKNOWN_TYPE))

    @staticmethod
    def build(waypoint: Waypoint) -> 'MapTile':

        return MapTile(uuid.uuid4(), waypoint)

    def __init__(self, id: uuid.UUID, waypoint: Waypoint):
        self.id = id
        self.waypoint = waypoint

        self.g_score = float('inf')  # Cost from start node
        self.h_score = 0  # Heuristic score
        self.f_score = float('inf')  # Total score (g_score + h_score)
        self.parent = None  # Parent node

        self.adjacent_tiles: list[MapTile] = []

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __hash__(self):
        return hash((self.waypoint.x, self.waypoint.y, self.waypoint.z))

    def __eq__(self, other):
        if isinstance(other, MapTile):
            return self.waypoint.x == other.waypoint.x and self.waypoint.y == other.waypoint.y and self.waypoint.z == other.waypoint.z

        return False

    def __str__(self):
        return f'Tile(x={self.waypoint.x}, y={self.waypoint.y}, z={self.waypoint.z})'

    def set_parent(self, node: 'MapTile'):
        self.parent = node

    def create_adjacent_tiles(self) -> None:
        for cardinal_point in range(4):
            if cardinal_point == 0:
                north_tile = MapTile.build(
                    Waypoint(
                        self.waypoint.x,
                        self.waypoint.y + 1,
                        self.waypoint.z,
                        Waypoint.UNKNOWN_TYPE
                    )
                )
                self.adjacent_tiles.append(north_tile)

                continue
            if cardinal_point == 1:
                south_tile = MapTile.build(
                    Waypoint(
                        self.waypoint.x,
                        self.waypoint.y - 1,
                        self.waypoint.z,
                        Waypoint.UNKNOWN_TYPE
                    )
                )
                self.adjacent_tiles.append(south_tile)

                continue
            if cardinal_point == 2:
                east_tile = MapTile.build(
                    Waypoint(
                        self.waypoint.x + 1,
                        self.waypoint.y,
                        self.waypoint.z,
                        Waypoint.UNKNOWN_TYPE
                    )
                )
                self.adjacent_tiles.append(east_tile)

                continue
            if cardinal_point == 3:
                west_tile = MapTile.build(
                    Waypoint(
                        self.waypoint.x - 1,
                        self.waypoint.y,
                        self.waypoint.z,
                        Waypoint.UNKNOWN_TYPE
                    )
                )
                self.adjacent_tiles.append(west_tile)

                continue

    def calculate_cost(self, initial: Waypoint, destination: Waypoint):
        self.h_score = self.waypoint.calculate_distance(destination)
        self.g_score = self.waypoint.calculate_distance(initial)

        self.f_score = self.h_score + self.g_score
