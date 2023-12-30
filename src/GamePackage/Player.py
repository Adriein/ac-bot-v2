from src.OperatingSystemPackage import Keyboard


class Player:
    def __init__(self, keyboard: Keyboard):
        self.__keyboard = keyboard

    def eat(self) -> None:
        self.__keyboard.press('v')

    def spell_heal(self, spell: str) -> None:
        self.__keyboard.press('r')
