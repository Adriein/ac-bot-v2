from .Creature import Creature


class GameContext:
    def __init__(self):
        self.__health = 0
        self.__mana = 0
        self.__is_attacking = False
        self.__creatures_in_range = list()

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
