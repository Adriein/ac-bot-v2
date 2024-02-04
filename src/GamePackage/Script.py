import json

from src.SharedPackage import Creature, Coordinate, Waypoint
from src.UtilPackage import LinkedList


class Script:
    __FILE_READ_MODE = 'r'
    __PLAYER_HOTKEY_CONFIG_JSON = 'src/Wiki/Player/player_config.json'

    __waypoints: LinkedList = LinkedList[Waypoint]()
    __creatures: list[Creature] = list()
    __player_config: dict = None

    __floor_levels: set[int] = set()

    def __init__(self, script_json_data: dict, player_config: dict):
        self.__player_config = player_config

        for creature in script_json_data['creatures']:
            self.__creatures.append(
                Creature(
                    creature['name'],
                    creature['priority'],
                    creature['runner'],
                    creature['loot'],
                    Coordinate(0, 0)
                )
            )

        for waypoint in script_json_data['walk']:
            x, y, z = waypoint[0].split(',')

            waypoint_type = waypoint[1]

            self.__floor_levels.add(int(z))

            self.__waypoints.append(Waypoint(int(x), int(y), int(z), waypoint_type))

    @staticmethod
    def load(name: str) -> 'Script':
        with open(name, Script.__FILE_READ_MODE) as file:
            script_data = json.load(file)

        with open(Script.__PLAYER_HOTKEY_CONFIG_JSON, Script.__FILE_READ_MODE) as file:
            player_config = json.load(file)

        return Script(script_data, player_config)

    def creatures(self) -> list[Creature]:
        return self.__creatures

    def waypoints(self) -> LinkedList[Waypoint]:
        return self.__waypoints

    def floors(self) -> set[int]:
        return self.__floor_levels

    def player_config(self) -> dict:
        return self.__player_config
