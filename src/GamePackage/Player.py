from src.OperatingSystemPackage import Keyboard


class Player:
    def __init__(self, keyboard: Keyboard, config: dict):
        self.__keyboard = keyboard
        self.__config = config

    def eat(self) -> None:
        self.__keyboard.press('v')

    def spell_heal(self, spell: str) -> None:
        self.__keyboard.press('r')

    def potion_heal(self) -> None:
        self.__keyboard.press('x')

    def config(self) -> dict:
        return self.__config
