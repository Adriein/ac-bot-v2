from src.SharedPackage.Creature import Creature


class GameContext:
    def __init__(self, health: int, mana: int, is_attacking: bool, creatures_in_range: list[Creature]):
        self.__health = health
        self.__mana = mana
        self.__is_attacking = is_attacking
        self.__creatures_in_range = creatures_in_range

    def set_health(self, health: int) -> None:
        self.__health = health

    def get_health(self) -> int:
        return self.__health

    def set_mana(self, mana: int) -> None:
        self.__mana = mana

    def get_mana(self) -> int:
        return self.__mana

    def set_is_attacking(self, is_attacking: bool) -> None:
        self.__is_attacking = is_attacking

    def get_is_attacking(self) -> bool:
        return self.__is_attacking

    def get_creatures_in_range(self) -> list[Creature]:
        return self.__creatures_in_range

    def __str__(self):
        return f"GameContext(health={self.get_health}, mana={self.get_mana}), is_attacking={self.get_is_attacking}), " \
               f"creatures_in_range={self.get_creatures_in_range})"
