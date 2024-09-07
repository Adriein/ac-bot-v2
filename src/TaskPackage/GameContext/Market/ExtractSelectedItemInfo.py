import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.SharedPackage import GameContext, ScreenRegion, Offer, Constants
from src.TaskPackage.Task import Task
from src.UtilPackage import GenericMapCollection
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

            item = context.get_scrapped_item()
            extraction_result = GenericMapCollection[Offer]()

            extraction_result.set(Constants.SELL_OFFER, Offer(Constants.SELL_OFFER))
            extraction_result.set(Constants.BUY_OFFER, Offer(Constants.BUY_OFFER))

            amount_screen_regions = self.__get_screen_regions(grey_frame, 'amount_column_anchor')

            self.__extract_row_offer(grey_frame, amount_screen_regions, extraction_result, "amount")

            price_screen_regions = self.__get_screen_regions(grey_frame, 'piece_price_column_anchor')

            self.__extract_row_offer(grey_frame, price_screen_regions, extraction_result, "unit_price")

            end_at_screen_region = self.__get_screen_regions(grey_frame, 'ends_at_column_anchor')

            self.__extract_row_offer(grey_frame, end_at_screen_region, extraction_result, "end_date")

            print(extraction_result.get(Constants.SELL_OFFER))
            print(extraction_result.get(Constants.BUY_OFFER))

            item.offers = [extraction_result.get(Constants.SELL_OFFER), extraction_result.get(Constants.BUY_OFFER)]

            raise KeyboardInterrupt

            Logger.debug("Updated context")
            Logger.debug(context, inspect_class=True)

            self.success()
            return context
        except ValueError:
            self.fail()
            raise KeyboardInterrupt
            return context

    def __get_screen_regions(self, grey_frame: np.ndarray, anchor_name: str) -> list[ScreenRegion]:
        anchor = Cv2File.load_image(f'src/Wiki/Ui/Market/{anchor_name}.png')

        height, width = anchor.shape

        match = cv2.matchTemplate(grey_frame, anchor, cv2.TM_CCOEFF_NORMED)

        multiple_loc = np.where(match >= 0.9)

        screen_regions = []

        for x, y in zip(*multiple_loc[::-1]):
            screen_region = ScreenRegion(
                start_x=x,
                end_x=x + width,
                start_y=y,
                end_y=y + height
            )

            screen_regions.append(screen_region)

        return screen_regions

    def __extract_row_offer(
            self,
            frame: np.ndarray,
            screen_regions: list[ScreenRegion],
            result_set: GenericMapCollection[Offer],
            column: str,
    ) -> None:
        for region, next_region in zip(screen_regions, screen_regions[1:]):
            if region.start_y < next_region.start_y:
                # The bottom of the column header
                start_y = region.end_y

                # The height of the row
                height = region.end_y - region.start_y
                end_y = region.end_y + height

                roi = frame[start_y:end_y, region.start_x:region.end_x]

                offer = result_set.get(Constants.SELL_OFFER)

                setattr(offer, column, self.__pyautogui.number(roi))

                result_set.set(Constants.SELL_OFFER, offer)

            start_y = next_region.end_y

            height = next_region.end_y - next_region.start_y
            end_y = next_region.end_y + height

            roi = frame[start_y:end_y, next_region.start_x:next_region.end_x]

            offer = result_set.get(Constants.BUY_OFFER)
            print(self.__pyautogui.number(roi))
            setattr(offer, column, self.__pyautogui.number(roi))

            result_set.set(Constants.BUY_OFFER, offer)

