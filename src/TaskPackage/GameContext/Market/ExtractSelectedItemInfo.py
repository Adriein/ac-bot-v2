import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext, ScreenRegion
from src.TaskPackage.Task import Task
from src.VendorPackage import Cv2File, PyAutoGui


class ExtractSelectedItemInfo(Task):
    def __str__(self) -> str:
        return f'ExtractSelectedItemInfo'

    def __init__(self, widget: GlobalGameWidgetContainer, pyautogui: PyAutoGui):
        super().__init__()
        self.__widget = widget
        self.__pyautogui = pyautogui
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        try:
            Logger.debug("Executing ExtractSelectedItemInfo")
            Logger.debug("Received context")
            Logger.debug(context, inspect_class=True)

            grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            self.__get_screen_region(grey_frame, 'piece_price_column_anchor')
            raise KeyboardInterrupt
            # current_health = self.__pyautogui.number(hp_roi)
            # current_health = int(self.__tesseract.number_img_to_string(hp_roi))


            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)

            self.success()
            return context
        except ValueError:
            self.fail()

            return context

    def __get_screen_region(self, grey_frame: np.ndarray, anchor_name: str) -> None:
        anchor = Cv2File.load_image(f'src/Wiki/Ui/Market/{anchor_name}.png')

        match = cv2.matchTemplate(grey_frame, anchor, cv2.TM_CCOEFF_NORMED)

        multiple_loc = np.where(match >= 0.9)

        screen_regions = []

        for x, y in zip(*multiple_loc[::-1]):
            screen_regions.append((x, y))


        print(screen_regions)
        height, width = anchor.shape


