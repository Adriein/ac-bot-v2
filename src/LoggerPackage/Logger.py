import traceback
import os
from typing import Any

from rich.console import Console
from rich.table import Table
from rich import inspect

from src.SharedPackage import Constants
from src.UtilPackage import Time
from src.UtilPackage import Array


class Logger:
    @staticmethod
    def info(message: str) -> None:
        print(f'[{Time.format(Time.now())}][AcBotv2][INFO]: {message}')

    @staticmethod
    def debug(message: str | Any, inspect_class=False) -> None:
        if Constants.DEBUG_MODE in os.environ:
            if not inspect_class:
                print(f'[{Time.format(Time.now())}][AcBotv2][DEBUG]: {message}')
                return

            inspect(message)

    @staticmethod
    def error(message: str, error: Exception) -> None:
        if Constants.DEV_MODE in os.environ or Constants.DEBUG_MODE in os.environ:
            console = Console()
            console.print_exception(show_locals=True)

            return

        if not message:
            message = 'Fatal Exception without message'

        print(f'[{Time.format(Time.now())}][AcBotv2][ERROR]: {message}')
        print(f'  [AcBotv2][TRACE]:')
        for index, stack_trace in enumerate(Array.reverse(traceback.format_tb(error.__traceback__))):
            stack_list = stack_trace.strip().replace("\n", "").split(",")
            print(f'    > [{index}] {stack_list[0]}')
            print(f'    > [{index}] {stack_list[1].strip()}')
            print(f'    > [{index}] {stack_list[2].strip()}')
            print("")

    @staticmethod
    def table(title: str, table: Table) -> None:
        print(f'[{Time.format(Time.now())}][AcBotv2][INFO]: {title}')

        console = Console()
        console.print(table)
