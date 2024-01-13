from src.LoggerPackage import Logger
from src.OperatingSystemPackage import Keyboard, Mouse
from src.SharedPackage import Creature
from src.VendorPackage import PyAutoGui


class Player:
    def __init__(self, keyboard: Keyboard, mouse: Mouse, config: dict, pyautogui: PyAutoGui):
        self.__keyboard = keyboard
        self.__mouse = mouse
        self.__config = config
        self.__pyautogui = pyautogui

    def precision_attack(self, creature: Creature) -> None:
        click_coordinate = creature.battle_list_position()

        self.__mouse.use_left_button(click_coordinate)

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
