from src.Shared.Creature import Creature


class GameContext:
    def __new__(cls, health: int, mana: int, is_attacking: bool, creatures_in_range: list[Creature]):
        cls.__health = health
        cls.__mana = mana
        cls.__is_attacking = is_attacking
        cls.__creatures_in_range = creatures_in_range

    def health(self) -> int:
        return self.__health

    def mana(self) -> int:
        return self.__mana

    def is_attacking(self) -> bool:
        return self.__is_attacking

    def creatures_in_range(self) -> list[Creature]:
        return self.__creatures_in_range

    def __str__(self):
        return f"GameContext(health={self.health}, mana={self.mana}), is_attacking={self.is_attacking}), creatures_in_range={self.creatures_in_range})"
