from time import sleep

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import Keyboard, Mouse
from src.SharedPackage import Creature, Coordinate, MoveCommand
from src.VendorPackage import PyAutoGui
from src.UtilPackage import Number


class Player:
    def __init__(
            self,
            keyboard: Keyboard,
            mouse: Mouse,
            config: dict,
            pyautogui: PyAutoGui
    ):
        self.__keyboard = keyboard
        self.__mouse = mouse
        self.__config = config
        self.__pyautogui = pyautogui

    def precision_attack(self, creature: Creature) -> None:
        click_coordinate = creature.battle_list_position()

        self.__mouse.use_left_button(click_coordinate)

        random_x = Number.random(100, 150)
        random_y = Number.random(30, 60)

        space_move = Coordinate(click_coordinate.x - random_x, click_coordinate.y + random_y)
        self.__mouse.move_mouse(space_move)

    def loot(self, coordinates: list[Coordinate]) -> None:
        self.__keyboard.key_down('shift')
        for coordinate in coordinates:
            self.__mouse.use_right_button(coordinate)

        self.__keyboard.key_up('shift')

    def eat(self) -> None:
        Logger.info('Eat food')
        self.__keyboard.press('v')

    def spell_heal(self, spell: str) -> None:
        Logger.info(f'Spell healing with {spell}')
        self.__keyboard.press('r')

    def potion_heal(self) -> None:
        Logger.info('Potion healing')
        self.__keyboard.press('y')

    def config(self) -> dict:
        return self.__config

    def move(self, command: MoveCommand) -> None:
        self.__keyboard.press(command.key)

    def rope(self, coordinates: Coordinate) -> None:
        self.__keyboard.press('f')
        self.__mouse.use_left_button(coordinates)

    def use_hand_stair(self, coordinates: Coordinate) -> None:
        self.__mouse.use_right_button(coordinates)

    def chase_opponent(self) -> None:
        self.__keyboard.press('g')

    def use_stealth_ring(self) -> None:
        Logger.info('Equip stealth ring')
        self.__keyboard.press('t')

    def open(self, coordinates: Coordinate) -> None:
        self.__mouse.use_right_button(coordinates)

    def left_click(self, coordinates: Coordinate) -> None:
        self.__mouse.use_left_button(coordinates)

    def write(self, word: str) -> None:
        letters = list(word)

        for letter in letters:
            if letter == "":
                self.__keyboard.press("space")
                continue

            self.__keyboard.press(letter)
            sleep(0.2)
