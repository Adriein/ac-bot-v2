import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext, Coordinate, ScreenRegion, ManualIterationInterrupt
from src.TaskPackage.Task import Task
from src.GamePackage import Player
from src.VendorPackage import Cv2File


class OpenMarketTask(Task):
    def __str__(self) -> str:
        return f'OpenMarketTask'

    def __init__(self, widget: GlobalGameWidgetContainer, player: Player):
        super().__init__()
        self.__widget = widget
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing OpenMarketTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if context.get_is_market_open():
            self.success()

            return context

        market_anchor = Cv2File.load_image(f'src/Wiki/Ui/Market/market_icon.png')

        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        match = cv2.matchTemplate(grey_frame, market_anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        height, width = market_anchor.shape

        market_region = ScreenRegion(
            start_x=x,
            end_x=x + width,
            start_y=y,
            end_y=y + height
        )

        self.__player.open(Coordinate.from_screen_region(market_region))

        context.set_is_market_open(True)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        raise ManualIterationInterrupt
