import numpy as np
import cv2

from src.LoggerPackage import Logger
from src.SharedPackage import GameContext, ScreenRegion, Creature, Coordinate
from src.TaskPackage.Task import Task
from src.OperatingSystemPackage import GlobalGameWidgetContainer
from src.UtilPackage import String
from src.VendorPackage import Cv2File


class ExtractBattleListDataTask(Task):
    def __str__(self) -> str:
        return f'ExtractBattleListDataTask'

    def __init__(self, container: GlobalGameWidgetContainer):
        super().__init__()
        self.__container = container
        self.__succeed = False
        self.__completed = False

    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        Logger.debug("Executing ExtractBattleListDataTask")
        Logger.debug("Received context")
        Logger.debug(context, inspect_class=True)

        widget = self.__container.battle_list_widget()

        battle_list_roi = frame[widget.start_y: widget.end_y, widget.start_x: widget.end_x]

        grey_battle_list_roi = cv2.cvtColor(battle_list_roi, cv2.COLOR_BGR2GRAY)

        results = list()

        for enemy in [Creature('wasp', 1, False, True, Coordinate(0, 0))]:
            enemy_path = f'src/Wiki/Ui/Mobs/{String.snake_to_camel_case(enemy.name())}/{enemy.name}_label.png'

            creature_template = Cv2File.load_image(enemy_path)

            match = cv2.matchTemplate(grey_battle_list_roi, creature_template, cv2.TM_CCOEFF_NORMED)

            # match_locations = (y_match_coords, x_match_coords) >= similarity more than threshold
            match_locations = np.where(match >= 0.9)

            # paired_match_locations = [(x, y), (x, y)]
            paired_match_locations = list(zip(*match_locations[::-1]))

            ordered_match_locations = sorted(paired_match_locations, key=lambda pair: pair[1], reverse=False)

            if ordered_match_locations:
                for (nearest_creature_battle_list_roi_x, nearest_creature_battle_list_roi_y) in ordered_match_locations:
                    creature_template_height, creature_template_width = creature_template.shape

                    frame_creature_position_start_x = widget.start_x + nearest_creature_battle_list_roi_x
                    frame_creature_position_start_y = widget.start_y + nearest_creature_battle_list_roi_y
                    frame_creature_end_x = frame_creature_position_start_x + creature_template_width
                    frame_creature_end_y = frame_creature_position_start_y + creature_template_height

                    battle_list_position = ScreenRegion(
                        frame_creature_position_start_x,
                        frame_creature_end_x,
                        frame_creature_position_start_y,
                        frame_creature_end_y
                    )

                    click_coordinate = Coordinate.from_screen_region(battle_list_position)

                    creature = Creature(
                        enemy.name(),
                        enemy.priority(),
                        enemy.is_runner(),
                        enemy.has_to_loot(),
                        click_coordinate
                    )

                    results.append(creature)

        context.set_creatures_in_range(results)

        Logger.debug("Updated context")
        Logger.debug(context, inspect_class=True)

        self.success()

        return context

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
