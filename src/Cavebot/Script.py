import json

from src.SharedPackage import Creature, Coordinate
from src.UtilPackage import LinkedList


class Script:
    __FILE_READ_MODE = 'r'
    __PLAYER_HOTKEY_CONFIG_JSON = 'src/Wiki/Player/player_hotkey_config.json'

    __waypoints: LinkedList = LinkedList()
    __creatures: list[Creature] = list()
    __hotkey_bindings: dict = None

    __floor_levels: set[int] = set()

    def __init__(self, script_json_data: dict, player_hotkey_config: dict):
        self.__hotkey_bindings = player_hotkey_config

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
            script_data = json.load(file)

        with open(Script.__PLAYER_HOTKEY_CONFIG_JSON, Script.__FILE_READ_MODE) as file:
            hotkey_binding = json.load(file)

        return Script(script_data, hotkey_binding)

    def __extract_z_level_from_waypoint(self, waypoint: str) -> None:
        x, y, z = waypoint.split(',')

        self.__floor_levels.add(int(z))

    def creatures(self) -> list[Creature]:
        return self.__creatures

    def waypoints(self) -> LinkedList:
        return self.__waypoints

    def floors(self) -> set[int]:
        return self.__floor_levels
