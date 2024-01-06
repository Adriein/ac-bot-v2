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

        anchor = Cv2File.load_image('src/Wiki/Ui/Battle/attack_creature_anchor.png', False)

        anchor_hsv = cv2.cvtColor(anchor, cv2.COLOR_BGR2HSV)

        # Use a color picker tool to identify the red color in the image
        red_color = (255, 0, 0)
        color_bgr = np.uint8([[[255, 0, 0]]])

        # Convert the red color to HSV
        red_hsv = cv2.cvtColor(color_bgr, cv2.COLOR_RGB2HSV)

        # Adjust the lower_red and upper_red arrays
        lower_red = np.array([red_hsv[0][0][0] - 30, 255, 255])
        upper_red = np.array([red_hsv[0][0][0] + 30, 255, 255])

        battle_list_roi_hsv = cv2.cvtColor(battle_list_roi, cv2.COLOR_BGR2HSV)

        # Apply color detection to the widget
        red_mask_battle_list_roi = cv2.inRange(battle_list_roi_hsv, lower_red, upper_red)
        red_mask_anchor_hsv = cv2.inRange(anchor_hsv, lower_red, upper_red)

        # Find contours of the yellow square
        contours, _ = cv2.findContours(red_mask_battle_list_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Crop the image to the largest contour
        x, y, w, h = cv2.boundingRect(largest_contour)
        cropped_image = red_mask_battle_list_roi[y - 2:y + h + 2, x - 2:x + w + 2]

        PyAutoGui.debug_image(cropped_image)
        PyAutoGui.debug_image(red_mask_anchor_hsv)

        # Calculate the template matching score
        result = cv2.matchTemplate(red_mask_battle_list_roi, red_mask_anchor_hsv, cv2.TM_CCOEFF_NORMED)

        [_, max_val, _, _] = cv2.minMaxLoc(result)
        print(max_val)
        raise SystemExit
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
