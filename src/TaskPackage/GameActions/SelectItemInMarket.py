from time import sleep

import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext, Coordinate, ScreenRegion, ManualIterationInterrupt
from src.TaskPackage.Task import Task
from src.GamePackage import Player
from src.VendorPackage import Cv2File

class SelectItemInMarket(Task):
    def __str__(self) -> str:
        return f'SelectItemInMarket'

    def __init__(self, widget: GlobalGameWidgetContainer, player: Player):
        super().__init__()
        self.__widget = widget
        self.__player = player
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing SelectItemInMarket")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if context.get_is_item_selected():
            self.success()

            return context

        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        item_list_anchor_screen_region = self.__get_screen_region(grey_frame, 'item_list')

        item_list_screen_region = ScreenRegion(
            start_x= item_list_anchor_screen_region.start_x,
            end_x= item_list_anchor_screen_region.end_x,
            start_y= item_list_anchor_screen_region.start_y,
            end_y=item_list_anchor_screen_region.end_y + 40
        )

        self.__player.left_click(Coordinate.from_screen_region(item_list_screen_region))

        context.set_is_item_selected(True)

        sleep(1)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        raise ManualIterationInterrupt

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