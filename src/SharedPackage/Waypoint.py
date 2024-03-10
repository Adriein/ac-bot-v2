from .Coordinate import Coordinate


class Waypoint:
    UNKNOWN_TYPE = 'unknown'
    HOLE_UP_TYPE = 'hole_up'
    HOLE_DOWN_TYPE = 'hole_down'
    STAIR_UP_TYPE = 'stair_up'
    STAIR_DOWN_TYPE = 'stair_down'
    HAND_STAIR_UP_TYPE = 'hand_stair_up'
    HAND_STAIR_DOWN_TYPE = 'hand_stair_down'

    @staticmethod
    def from_string(string_waypoint: str, type: str) -> 'Waypoint':
        x, y, z = string_waypoint.split(',')

        return Waypoint(int(x), int(y), int(z), type)

    def __init__(self, x: int, y: int, z: int, type: str):
        self.x = x
        self.y = y
        self.z = z
        self.type = type

    def __str__(self):
        return f'x={self.x} y={self.y} z={self.z} type={self.type}'

    def __eq__(self, other):
        if isinstance(other, Waypoint):
            return self.x == other.x and self.y == other.y and self.z == other.z

        return False

    def hash(self) -> str:
        return f'{self.x}{self.y}{self.z}'

    def to_string(self) -> str:
        return f'{self.x},{self.y},{self.z}'

    def to_coordinate(self) -> Coordinate:
        return Coordinate(self.x - 31744, self.y - 30976)

    def cardinal_direction_between_waypoints(self, destination: 'Waypoint') -> str:
        if destination.x > self.x:
            return 'east'

        if destination.x < self.x:
            return 'west'

        if destination.y < self.y:
            return 'north'

        if destination.y > self.y:
            return 'south'

    def is_floor_change_type(self) -> bool:
        floor_change_type = [
            self.HOLE_UP_TYPE,
            self.HOLE_DOWN_TYPE,
            self.STAIR_UP_TYPE,
            self.STAIR_DOWN_TYPE,
            self.HAND_STAIR_UP_TYPE,
            self.HAND_STAIR_DOWN_TYPE,
        ]

        return self.type in floor_change_type

    def is_auto_floor_down(self) -> bool:
        floor_change_type = [
            self.HOLE_DOWN_TYPE,
            self.STAIR_DOWN_TYPE,
            self.HAND_STAIR_DOWN_TYPE,
        ]

        return self.type in floor_change_type

    def is_auto_floor_up(self) -> bool:
        floor_change_type = [
            self.STAIR_UP_TYPE,
        ]

        return self.type in floor_change_type

    def is_in_same_floor(self, other: 'Waypoint') -> bool:
        return self.z == other.z

    def calculate_distance(self, other: 'Waypoint') -> float:
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5
