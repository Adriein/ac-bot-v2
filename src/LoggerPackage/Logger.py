import traceback
import os
from rich.console import Console
from rich.table import Table

from src.SharedPackage import Constants
from src.UtilPackage import Time
from src.UtilPackage import Array


class Logger:
    @staticmethod
    def info(message: str) -> None:
        print(f'[{Time.now()}][AcBotv2][INFO]: {message}')

    @staticmethod
    def debug(message: str) -> None:
        if os.environ[Constants.DEBUG_MODE]:
            print(f'[{Time.now()}][AcBotv2][DEBUG]: {message}')

    @staticmethod
    def error(message: str, error: Exception) -> None:
        if os.environ[Constants.DEV_MODE]:
            console = Console()
            console.print_exception(show_locals=True)

            return

        if not message:
            message = 'Fatal Exception without message'

        print(f'[{Time.now()}][AcBotv2][ERROR]: {message}')
        print(f'  [AcBotv2][TRACE]:')
        for index, stack_trace in enumerate(Array.reverse(traceback.format_tb(error.__traceback__))):
            stack_list = stack_trace.strip().replace("\n", "").split(",")
            print(f'    > [{index}] {stack_list[0]}')
            print(f'    > [{index}] {stack_list[1].strip()}')
            print(f'    > [{index}] {stack_list[2].strip()}')
            print("")

    @staticmethod
    def table(title: str, table: Table) -> None:
        print(f'[{Time.now()}][AcBotv2][DEBUG]: {title}')

        console = Console()
        console.print(table)
