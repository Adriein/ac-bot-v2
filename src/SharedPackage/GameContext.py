from .Creature import Creature
from datetime import datetime


class GameContext:
    def __str__(self):
        return f"GameContext"

    def __init__(self):
        self.__health = 0
        self.__mana = 0
        self.__last_meal_time = None
        self.__next_meal_time = None

        self.__is_attacking = False

        self.__creatures_in_range = list()
        self.__script_enemies = list()

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

    def set_creatures_in_range(self, creatures: list[Creature]) -> None:
        self.__creatures_in_range = creatures

    def get_creatures_in_range(self) -> list[Creature]:
        return self.__creatures_in_range

    def get_script_enemies(self) -> list[Creature]:
        return self.__script_enemies

    def set_last_meal_time(self, meal_time: datetime) -> None:
        self.__last_meal_time = meal_time

    def get_last_meal_time(self) -> datetime:
        return self.__last_meal_time

    def set_next_meal_time(self, meal_time: datetime) -> None:
        self.__next_meal_time = meal_time

    def get_next_meal_time(self) -> datetime:
        return self.__next_meal_time

