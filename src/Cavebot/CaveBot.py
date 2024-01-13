from src.GamePackage import Player, Script
from src.OperatingSystemPackage import Monitor, GlobalGameWidgetContainer
from src.SharedPackage import GameContext
from src.TaskPackage import TaskResolver, ExtractGameContextDataTask, AttackTask, HealingTask
from src.VendorPackage import TesseractOcr


class CaveBot:

    def __init__(
            self,
            monitor: Monitor,
            resolver: TaskResolver,
            widget: GlobalGameWidgetContainer,
            tesseract: TesseractOcr
    ):
        self.__monitor = monitor
        self.__resolver = resolver
        self.__widget = widget
        self.__tesseract = tesseract

    def start(self, game_context: GameContext, player: Player) -> None:
        screenshot = self.__monitor.screenshot()

        # 1. extract game context
        extract_game_context_data_task = ExtractGameContextDataTask(self.__resolver, self.__widget, self.__tesseract)
        self.__resolver.queue(extract_game_context_data_task)

        self.__resolver.resolve(game_context, screenshot)

        # 2. auto healing
        healing_task = HealingTask(player)
        # self.__resolver.queue(healing_task)

        # 3. auto attacking
        attack_task = AttackTask(self.__resolver, player)
        self.__resolver.queue(attack_task)

        # 4. auto looting

        self.__resolver.resolve(game_context, screenshot)
