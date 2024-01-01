from src.SharedPackage.Coordinate import Coordinate


class Creature:
    def __init__(self, name: str, priority: int, runner: bool, has_to_loot: bool, battle_list_position: Coordinate):
        self.__name = name
        self.__priority = priority
        self.__runner = runner
        self.__has_to_loot = has_to_loot
        self.__battle_list_position = battle_list_position

    def __str__(self):
        return (f'Creature(name={self.__name}, runner={self.__runner}, has_to_loot={self.__has_to_loot}, '
                f'battle_list_position={self.__battle_list_position})')

    def name(self) -> str:
        return self.__name

    def priority(self) -> int:
        return self.__priority

    def is_runner(self) -> bool:
        return self.__runner

    def has_to_loot(self) -> bool:
        return self.__has_to_loot

    def battle_list_position(self) -> Coordinate:
        return self.__battle_list_position
