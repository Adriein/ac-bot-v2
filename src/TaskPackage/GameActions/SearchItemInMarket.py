from time import sleep

import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext, Coordinate, ScreenRegion, ManualIterationInterrupt
from src.TaskPackage.Task import Task
from src.GamePackage import Player
from src.VendorPackage import Cv2File

class SearchItemInMarket(Task):
    def __str__(self) -> str:
        return f'SearchItemInMarket'

    def __init__(self, widget: GlobalGameWidgetContainer, player: Player):
        super().__init__()
        self.__widget = widget
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing SearchItemInMarket")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if not context.get_is_market_open():
            self.success()

            return context

        market_cancel_search_anchor = Cv2File.load_image(f'src/Wiki/Ui/Market/market_cancel_search.png')

        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        match = cv2.matchTemplate(grey_frame, market_cancel_search_anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        height, width = market_cancel_search_anchor.shape

        close_button_region = ScreenRegion(
            start_x=x,
            end_x=x + width,
            start_y=y,
            end_y=y + height
        )

        close_button_coordinate = Coordinate.from_screen_region(close_button_region)

        self.__player.left_click(Coordinate(close_button_coordinate.x - 20, close_button_coordinate.y))

        sleep(0.5)

        self.__player.write('honeycomb')

        context.set_is_scrapping_item_info(True)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        raise KeyboardInterrupt
        raise ManualIterationInterrupt
