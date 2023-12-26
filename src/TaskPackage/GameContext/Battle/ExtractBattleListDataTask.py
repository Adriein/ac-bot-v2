import numpy as np
import pytesseract
import cv2

from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task
from src.OperatingSystemPackage import GlobalGameWidgetContainer


class ExtractBattleListDataTask(Task):
    def __init__(self, container: GlobalGameWidgetContainer):
        super().__init__()
        self.__container = container
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        widget = self.__container.battle_list_widget()

        print(widget)

        battle_list_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x]

        # Window name in which image is displayed
        window_name = 'image'

        # Using cv2.imshow() method
        # Displaying the image
        cv2.imshow(window_name, battle_list_roi)

        # waits for user to press any key
        # (this is necessary to avoid Python kernel form crashing)
        cv2.waitKey(0)

        # closing all open windows
        cv2.destroyAllWindows()

        battle_list_rgb = cv2.cvtColor(battle_list_roi, cv2.COLOR_BGR2RGB)

        text = pytesseract.image_to_string(battle_list_rgb)

        print(text)

        self.success()
        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
