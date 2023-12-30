import json

from src.SharedPackage import Creature, Coordinate
from src.UtilPackage import LinkedList


class Script:
    __FILE_READ_MODE = 'r'

    __waypoints: LinkedList = LinkedList()
    __creatures: list[Creature] = list()

    FLOORS_LEVELS: set[int] = set()

    def __init__(self, script_json_data):
        for creature in script_json_data['creatures']:
            self.__creatures.append(
                Creature(
                    creature['name'],
                    creature['runner'],
                    creature['loot'],
                    Coordinate(0, 0)
                )
            )

        for waypoint in script_json_data['walk']:
            self.__extract_z_level_from_waypoint(waypoint[0])
            self.__waypoints.append(waypoint)

    @staticmethod
    def load(name: str) -> 'Script':
        with open(name, Script.__FILE_READ_MODE) as file:
            data = json.load(file)

        return Script(data)

    def __extract_z_level_from_waypoint(self, waypoint: str) -> None:
        x, y, z = waypoint.split(',')

        self.FLOORS_LEVELS.add(int(z))

    def creatures(self) -> list[Creature]:
        return self.__creatures

    def waypoints(self) -> LinkedList:
        return self.__waypoints
