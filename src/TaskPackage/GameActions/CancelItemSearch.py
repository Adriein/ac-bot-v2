from time import sleep

import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext, Coordinate, ScreenRegion, MarketItem
from src.TaskPackage.Task import Task
from src.GamePackage import Player
from src.VendorPackage import Cv2File

class CancelItemSearch(Task):
    def __str__(self) -> str:
        return f'CancelItemSearch'

    def __init__(self, widget: GlobalGameWidgetContainer, player: Player):
        super().__init__()
        self.__widget = widget
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing CancelItemSearch")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)


        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        close_button_region = self.__get_screen_region(grey_frame, 'market_cancel_search')

        close_button_coordinate = Coordinate.from_screen_region(close_button_region)

        self.__player.left_click(Coordinate(close_button_coordinate.x, close_button_coordinate.y))

        sleep(0.5)

        context.set_is_item_searched(False)
        context.set_is_item_selected(False)
        context.set_scrapped_item(None)

        item_list = context.get_trade_items()

        if not item_list.peak_next():
            raise KeyboardInterrupt

        item_list.next()

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()
        return context

    def __get_screen_region(self, grey_frame: np.ndarray, anchor_name: str) -> ScreenRegion:
        anchor = Cv2File.load_image(f'src/Wiki/Ui/Market/{anchor_name}.png')

        match = cv2.matchTemplate(grey_frame, anchor, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (x, y) = max_coordinates

        height, width = anchor.shape

        return ScreenRegion(
            start_x=x,
            end_x=x + width,
            start_y=y,
            end_y=y + height
        )