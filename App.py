from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import Kernel, Monitor, GlobalGameWidgetContainer, Keyboard
from src.VendorPackage import PyAutoGui, TesseractOcr
from src.Cavebot import CaveBot
from src.Train import AutoTrainer
from src.TaskPackage import TaskResolver
from src.SharedPackage import Constants, GameContext

from rich.table import Table
import argparse
import os


class TibiaAcBot:
    def __init__(self):
        self.__kernel = None
        self.__monitor = None
        self.__keyboard = None
        self.__global_widget_container = None
        self.__task_resolver = None
        self.__pyautogui = None
        self.__tesseract = None

        self.__collect_program_arguments()
        self.__setup_global()

    def init(self) -> None:
        try:
            Logger.info('Started...')
            Logger.info('Press Ctrl+C to stop the execution')

            player = Player(self.__keyboard, dict())
            game_context = GameContext()

            if Constants.TRAIN_MODE not in os.environ:
                cavebot = CaveBot(
                    self.__monitor,
                    self.__keyboard,
                    self.__task_resolver,
                    self.__global_widget_container,
                    self.__tesseract
                )

                cavebot.start(game_context, player)

                return

            auto_trainer = AutoTrainer(
                self.__monitor,
                self.__keyboard,
                self.__task_resolver,
                self.__global_widget_container,
                self.__tesseract
            )

            auto_trainer.start(game_context, player)

        except KeyboardInterrupt:
            Logger.info('Graceful shutdown')
            raise SystemExit
        except Exception as error:
            Logger.error(str(error), error)
            raise SystemExit from error

    def __setup_global(self) -> None:
        Logger.info('Setup Global Config')
        Logger.info('Creating Kernel...')
        self.__kernel = os_kernel = Kernel()

        Logger.info('Creating PyAutoGui...')
        self.__pyautogui = PyAutoGui()

        Logger.info('Creating Monitor...')
        self.__monitor = Monitor(os_kernel, self.__pyautogui)

        Logger.info('Creating Tesseract..')
        self.__tesseract = TesseractOcr()

        Logger.info('Creating Keyboard..')
        self.__keyboard = Keyboard(self.__kernel)

        Logger.info('Locating Widgets...')
        self.__global_widget_container = GlobalGameWidgetContainer(self.__monitor, self.__pyautogui)

        Logger.info('Initializing TaskResolver...')
        self.__task_resolver = TaskResolver()

        self.__log_global_setup_resume()

    def __log_global_setup_resume(self) -> None:
        table = Table()
        table.add_column("Task", justify="left", style="magenta", no_wrap=True)
        table.add_column("Result", justify="left", style="green")

        table.add_row("Creating Kernel", "OK")
        table.add_row("Creating Monitor", "OK")
        table.add_row("Locating Widgets", "OK")
        table.add_row("Initializing TaskResolver", "OK")

        Logger.table('Global Setup Resume', table)

    def __collect_program_arguments(self) -> None:
        Logger.info('Collecting program arguments...')

        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--dev',
            action="store_true",
            help='Indicate that program should start in dev mode'
        )

        parser.add_argument(
            '--debug',
            action="store_true",
            help='Indicate that program should start in debug mode'
        )

        parser.add_argument(
            '--train',
            action="store_true",
            help='Indicate that program should start in training mode'
        )

        if parser.parse_args():
            table = Table()
            table.add_column("Argument", justify="left", style="magenta", no_wrap=True)
            table.add_column("Value", justify="left", style="green")

            if parser.parse_args().train:
                os.environ[Constants.TRAIN_MODE] = Constants.TRAIN_MODE
                table.add_row("--train", Constants.TRAIN_MODE)

            if parser.parse_args().debug:
                os.environ[Constants.DEBUG_MODE] = Constants.DEBUG_MODE
                table.add_row("--debug", Constants.DEBUG_MODE)

            if parser.parse_args().dev:
                os.environ[Constants.DEV_MODE] = Constants.DEV_MODE
                table.add_row("--dev", Constants.DEV_MODE)

            Logger.table('Program Arguments Resume', table)


TibiaAcBot().init()

'''
1. enemies in the battle list?
2. attack
3. need healing?
4. heal
'''

'''
first check status of the game and queue taks with prio
then resolve the tasks and loop again
'''
