from .Coordinate import Coordinate


class Waypoint:
    UNKNOWN_TYPE = 'unknown'
    HOLE_UP_TYPE = 'hole_up'
    HOLE_DOWN_TYPE = 'hole_down'
    STAIR_UP_TYPE = 'stair_up'
    STAIR_DOWN_TYPE = 'stair_down'

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
            return self.x == other.x and self.y == other.y and self.z == other.z and self.type == other.type

        return False

    def to_string(self) -> str:
        return f'{self.x},{self.y},{self.z}'

    def to_coordinate(self) -> Coordinate:
        return Coordinate(self.x - 31744, self.y - 30976)
