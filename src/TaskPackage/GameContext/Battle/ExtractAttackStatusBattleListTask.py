import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.VendorPackage import Cv2File


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

        previous_context = GameContext.copy(context)

        self.__determine_is_attacking(context, frame)

        self.__assert_creature_has_been_killed(previous_context, context)

        self.success()

        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed

    def __assert_creature_has_been_killed(self, previous_context: GameContext, actual_context: GameContext) -> None:
        if previous_context.get_is_attacking() and not actual_context.get_is_attacking():
            actual_context.set_pending_loot(True)

            Logger.debug("Updated context has a creature pending to loot")
            Logger.debug(actual_context, inspect_class=True)

    def __determine_is_attacking(self, context: GameContext, frame: np.ndarray) -> None:
        widget = self.__container.battle_list_widget()

        battle_list_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x]

        anchor = Cv2File.load_image('src/Wiki/Ui/Battle/attack_creature_anchor.png', False)

        anchor_hsv = cv2.cvtColor(anchor, cv2.COLOR_BGR2HSV)

        red_color_bgr = np.uint8([[[255, 0, 0]]])

        red_hsv = cv2.cvtColor(red_color_bgr, cv2.COLOR_RGB2HSV)

        lower_red = np.array([red_hsv[0][0][0] - 30, 255, 255])
        upper_red = np.array([red_hsv[0][0][0] + 30, 255, 255])

        battle_list_roi_hsv = cv2.cvtColor(battle_list_roi, cv2.COLOR_BGR2HSV)

        # Apply color detection to the battle list
        red_mask_battle_list_roi = cv2.inRange(battle_list_roi_hsv, lower_red, upper_red)
        red_mask_anchor_hsv = cv2.inRange(anchor_hsv, lower_red, upper_red)

        result = cv2.matchTemplate(red_mask_battle_list_roi, red_mask_anchor_hsv, cv2.TM_CCOEFF_NORMED)

        [_, max_val, _, _] = cv2.minMaxLoc(result)

        if max_val >= 0.4:
            context.set_is_attacking(True)

            Logger.debug("Updated context is attacking")
            Logger.debug(context, inspect_class=True)

            return

        context.set_is_attacking(False)

        Logger.debug("Updated context is not attacking")
        Logger.debug(context, inspect_class=True)

