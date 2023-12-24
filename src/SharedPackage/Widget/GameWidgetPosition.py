from src.SharedPackage.ScreenRegion import ScreenRegion


class GameWidgetPosition:
    def __init__(self, battle_list: ScreenRegion):
        self.__battle_list_location = battle_list

    def battle_list_location(self) -> ScreenRegion:
        return self.__battle_list_location

    def __str__(self):
        return f"GameWidgetPosition(battle_list_location=(start_x={self.__battle_list_location.start_x}, " \
               f"end_x={self.__battle_list_location.end_x}, start_y={self.__battle_list_location.start_y} " \
               f"end_y={self.__battle_list_location.end_y}))"
