import cv2
import numpy as np
import pyautogui
import math

from src.SharedPackage import ScreenRegion, Constants
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

        return ScreenRegion(start_x=frame_start_x, end_x=frame_end_x, start_y=frame_start_y, end_y=frame_end_y)

    def screen_size(self) -> (int, int):
        return pyautogui.size()

    def __calculate_battle_list_height(self, monitor_dimensions: tuple[int, int]) -> int:
        [width, _] = monitor_dimensions

        return (width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_BATTLE_LIST_WIDGET_HEIGHT
