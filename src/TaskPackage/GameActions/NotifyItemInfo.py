import numpy as np
import urllib.request
import urllib.parse

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task

class NotifyItemInfo(Task):
    def __str__(self) -> str:
        return f'NotifyItemInfo'

    def __init__(self, widget: GlobalGameWidgetContainer,):
        super().__init__()
        self.__widget = widget
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing NotifyItemInfo")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        url = 'https://api.example.com/data'
        data = {'key': 'value', 'another_key': 'another_value'}

        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data=data)

        with urllib.request.urlopen(req) as response:
            body = response.read()
            print(body.decode('utf-8'))


        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context
