import cv2
import numpy as np
import pyautogui
import math

from src.SharedPackage import ScreenRegion, Constants, Coordinate
from src.VendorPackage.Cv2File import Cv2File


class PyAutoGui:
    @staticmethod
    def debug_image(frame: np.ndarray) -> None:
        # Window name in which image is displayed
        window_name = 'image'

        # Using cv2.imshow() method
        # Displaying the image
        cv2.imshow(window_name, frame)

        # waits for user to press any key
        # (this is necessary to avoid Python kernel form crashing)
        cv2.waitKey(0)

        # closing all open windows
        cv2.destroyAllWindows()

    def __init__(self):
        pass

    def locate_battle_list_widget(self, frame: np.ndarray, monitor_dimensions: tuple[int, int]) -> ScreenRegion:
        grey_scale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        region = pyautogui.locate(
            'src/Wiki/Ui/Battle/battle_list.png',
            grey_scale_frame, confidence=0.8,
            grayscale=True
        )

        widget_height = int(self.__calculate_battle_list_height(monitor_dimensions))

        start_x = region.left
        end_x = region.left + region.width
        start_y = region.top
        end_y = region.top + region.height + widget_height

        return ScreenRegion(start_x, end_x, start_y, end_y)

    def locate_health_widget(self, frame: np.ndarray, monitor_dimensions: tuple[int, int]) -> ScreenRegion:
        [width, height] = monitor_dimensions

        stats_pixel_width = math.ceil(width * 20 / 100)
        stats_pixel_height = math.ceil(height / 2)

        hp_region = ScreenRegion(
            start_x=width - stats_pixel_width,
            end_x=width,
            start_y=0,
            end_y=stats_pixel_height
        )

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        hp_roi = frame[hp_region.start_y: hp_region.end_y, hp_region.start_x: hp_region.end_x]

        hp_stat_template = Cv2File.load_image('src/Wiki/Stat/hp.png')

        match = cv2.matchTemplate(hp_roi, hp_stat_template, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (start_x, start_y) = max_coordinates

        height, width = hp_stat_template.shape

        frame_start_x = hp_region.start_x + start_x
        frame_start_y = hp_region.start_y + start_y
        frame_end_x = frame_start_x + width
        frame_end_y = frame_start_y + height

        [start_x_addition, end_x_addition] = self.__calculate_stat_widget_number_position(monitor_dimensions)

        return ScreenRegion(
            start_x=frame_start_x + start_x_addition,
            end_x=frame_end_x + end_x_addition,
            start_y=frame_start_y,
            end_y=frame_end_y
        )

    def locate_mana_widget(self, frame: np.ndarray, monitor_dimensions: tuple[int, int]) -> ScreenRegion:
        [width, height] = monitor_dimensions

        stats_pixel_width = math.ceil(width * 20 / 100)
        stats_pixel_height = math.ceil(height / 2)

        mana_region = ScreenRegion(
            start_x=width - stats_pixel_width,
            end_x=width,
            start_y=0,
            end_y=stats_pixel_height
        )

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        hp_roi = frame[mana_region.start_y: mana_region.end_y, mana_region.start_x: mana_region.end_x]

        hp_stat_template = Cv2File.load_image('src/Wiki/Stat/mana.png')

        match = cv2.matchTemplate(hp_roi, hp_stat_template, cv2.TM_CCOEFF_NORMED)

        [_, _, _, max_coordinates] = cv2.minMaxLoc(match)

        (start_x, start_y) = max_coordinates

        height, width = hp_stat_template.shape

        frame_start_x = mana_region.start_x + start_x
        frame_start_y = mana_region.start_y + start_y
        frame_end_x = frame_start_x + width
        frame_end_y = frame_start_y + height

        [start_x_addition, end_x_addition] = self.__calculate_stat_widget_number_position(monitor_dimensions)

        return ScreenRegion(
            start_x=frame_start_x + start_x_addition,
            end_x=frame_end_x + end_x_addition,
            start_y=frame_start_y,
            end_y=frame_end_y
        )

    def screen_size(self) -> (int, int):
        return pyautogui.size()

    def __calculate_battle_list_height(self, monitor_dimensions: tuple[int, int]) -> int:
        [width, _] = monitor_dimensions

        return (width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_BATTLE_LIST_WIDGET_HEIGHT

    def __calculate_stat_widget_number_position(self, monitor_dimensions: tuple[int, int]) -> tuple[int, int]:
        [width, _] = monitor_dimensions

        start_number = (
                                   width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_STAT_WIDGET_ANCHOR_TO_START_NUMBER
        end_number = (width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_STAT_WIDGET_ANCHOR_TO_END_NUMBER

        return int(start_number), int(end_number)

    def number(self, confidence: float, number_roi: np.array) -> int:
        number_coincidence = [(0, 0)]

        for number in range(10):
            number_image = Cv2File.load_image(f'src/Wiki/Ui/Number/{number}.png')

            match = cv2.matchTemplate(number_image, number_roi, cv2.TM_CCOEFF_NORMED)

            [_, max_coincidence, _, _] = cv2.minMaxLoc(match)

            if self.__ensure_confidence_threshold(confidence, max_coincidence):
                continue

            if self.__is_not_better_match(number_coincidence, max_coincidence):
                continue

            number_coincidence.remove(number_coincidence[0])

            number_coincidence.append((max_coincidence, number))

        print(number_coincidence)
        raise Exception
        if not number_coincidence:
            raise Exception

        if self.__ensure_some_match(coincidence_found=number_coincidence[0][0]):
            raise Exception

        return number_coincidence[0][1]

    def __ensure_confidence_threshold(self, client_provided_confidence: float, coincidence_found: float) -> bool:
        return coincidence_found < client_provided_confidence

    def __ensure_some_match(self, coincidence_found: float) -> bool:
        return coincidence_found <= 0.5

    def __is_not_better_match(self, number_coincidence: list[tuple[any, int]], coincidence_found: float) -> bool:
        return number_coincidence[0][0] > coincidence_found
