from src.LoggerPackage import Logger
from src.OperatingSystemPackage import Keyboard


class Player:
    def __init__(self, keyboard: Keyboard, config: dict):
        self.__keyboard = keyboard
        self.__config = config

    def eat(self) -> None:
        Logger.info('Eat food')
        self.__keyboard.press('v')

    def spell_heal(self, spell: str) -> None:
        Logger.info(f'Spell healing with {spell}')
        self.__keyboard.press('r')

    def potion_heal(self) -> None:
        Logger.info('Potion healing')
        self.__keyboard.press('x')

    def config(self) -> dict:
        return self.__config
