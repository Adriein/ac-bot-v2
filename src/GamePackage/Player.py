from src.OperatingSystemPackage import Keyboard


class Player:
    def __init__(self, keyboard: Keyboard):
        self.__keyboard = keyboard

    def eat(self) -> None:
        pass

    def spell_heal(self, spell: str) -> None:
        pass
