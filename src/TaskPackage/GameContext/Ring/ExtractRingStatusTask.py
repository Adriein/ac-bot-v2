import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.VendorPackage import PyAutoGui


class ExtractRingStatusTask(Task):
    def __str__(self) -> str:
        return f'ExtractRingStatusTask'

    def __init__(self, container: GlobalGameWidgetContainer):
        super().__init__()
        self.__container = container
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing ExtractRingStatusTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if not context.get_has_to_wear_ring():
            self.success()

            return context

        if self.__is_ring_equipped(frame):
            context.set_is_ring_equipped(True)

            self.success()

            return context

        context.set_is_ring_equipped(False)

        self.success()

        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed

    def __is_ring_equipped(self, frame: np.array) -> bool:
        widget = self.__container.ring_widget()

        frame_roi = frame[widget.start_y + 30 :widget.end_y + 30, widget.start_x + 30:widget.end_x + 30]

        PyAutoGui.debug_image(frame_roi)

        raise Exception

        hsv_image = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for blue color in HSV
        lower_blue = np.array([220, 67, 76])
        upper_blue = np.array([220, 67, 72])

        # Create a mask based on the color threshold
        mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

        # Count the number of green pixels
        blue_pixel_count = cv2.countNonZero(mask)

        # Determine if the image contains blue color
        if blue_pixel_count > 0:
            return True

        return False
