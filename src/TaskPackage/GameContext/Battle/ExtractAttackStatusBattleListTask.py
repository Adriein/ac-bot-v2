import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.VendorPackage import Cv2File, PyAutoGui


class ExtractAttackStatusBattleListTask(Task):
    def __str__(self) -> str:
        return f'ExtractAttackStatusBattleListTask'

    def __init__(self, container: GlobalGameWidgetContainer):
        super().__init__()
        self.__container = container
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing ExtractAttackStatusBattleListTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        widget = self.__container.battle_list_widget()

        battle_list_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x]

        anchor = Cv2File.load_image('src/Wiki/Ui/Battle/attacking_creature_anchor.png', False)

        anchor_hsv = cv2.cvtColor(anchor, cv2.COLOR_BGR2HSV)
        battle_list_roi_hsv = cv2.cvtColor(battle_list_roi, cv2.COLOR_BGR2HSV)
        PyAutoGui.debug_image(battle_list_roi_hsv)
        PyAutoGui.debug_image(anchor_hsv)
        # Extract the red pixels from the template
        lower_red = np.array([140, 100, 100])  # Yellow
        upper_red = np.array([200, 255, 255])  # Yellow

        red_mask_anchor = cv2.inRange(anchor_hsv, lower_red, upper_red)

        # Apply color detection to the widget
        red_mask_battle_list_roi = cv2.inRange(battle_list_roi_hsv, lower_red, upper_red)
        PyAutoGui.debug_image(red_mask_battle_list_roi)
        # Segment the widget image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        red_segments = cv2.dilate(red_mask_battle_list_roi, kernel, iterations=2)

        for segment in red_segments:
            # Extract the red area from the segment
            red_area = cv2.bitwise_and(segment, red_mask_anchor)

            # Calculate the template matching score
            result = cv2.matchTemplate(red_area, red_mask_anchor, cv2.TM_CCOEFF_NORMED)

            [max_val, _, _, _] = cv2.minMaxLoc(result)

            if max_val >= 0.9:
                context.set_is_attacking(True)

                Logger.debug("Updated context is attacking")
                Logger.debug(context, inspect_class=True)

                self.success()

                return context

        context.set_is_attacking(False)

        Logger.debug("Updated context is not attacking")
        Logger.debug(context, inspect_class=True)

        self.success()

        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
