import cv2
import numpy as np
import pyautogui

from src.SharedPackage import ScreenRegion, Constants


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

        widget_height = self.__calculate_battle_list_height(monitor_dimensions)

        start_x = region.left
        end_x = region.left + region.width
        start_y = region.top
        end_y = region.top + region.height + widget_height

        return ScreenRegion(start_x, end_x, start_y, end_y)

    def screen_size(self) -> (int, int):
        return pyautogui.size()

    def __calculate_battle_list_height(self, monitor_dimensions: tuple[int, int]) -> int:
        [width, _] = monitor_dimensions

        return (width / Constants.REFERENCE_WINDOW_WIDTH) * Constants.REFERENCE_BATTLE_LIST_WIDGET_HEIGHT
