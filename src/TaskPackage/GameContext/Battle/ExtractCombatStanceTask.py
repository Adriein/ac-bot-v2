import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.SharedPackage import GameContext, Constants
from src.TaskPackage.Task import Task
from src.OperatingSystemPackage import GlobalGameWidgetContainer


class ExtractCombatStanceTask(Task):
    def __str__(self) -> str:
        return f'ExtractCombatStanceTask'

    def __init__(self, container: GlobalGameWidgetContainer):
        super().__init__()
        self.__container = container
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing ExtractCombatStanceTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        if self.__is_chasing_opponent_activated(frame):
            context.set_combat_stance(Constants.CHASE_COMBAT_STANCE)

            self.success()

            return context

        context.set_combat_stance(Constants.IDLE_COMBAT_STANCE)

        self.success()

        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed

    def __is_chasing_opponent_activated(self, frame: np.array) -> bool:
        (start_x, end_x, start_y, end_y) = self.__container.combat_stance_widget()

        frame_roi = frame[start_y:end_y, start_x:end_x]

        hsv_image = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for green color in HSV
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([70, 255, 255])

        # Create a mask based on the color threshold
        mask = cv2.inRange(hsv_image, lower_green, upper_green)

        # Count the number of green pixels
        green_pixel_count = cv2.countNonZero(mask)

        # Determine if the image contains green color
        if green_pixel_count > 0:
            return True

        return False
