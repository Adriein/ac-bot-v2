from src.OperatingSystemPackage import Monitor, GlobalGameWidgetContainer
from src.SharedPackage import GameContext
from src.TaskPackage import TaskResolver, ExtractGameContextDataTask, AttackTask, HealingTask
from src.VendorPackage import TesseractOcr


class CaveBot:

    def __init__(self, monitor: Monitor, resolver: TaskResolver, widget: GlobalGameWidgetContainer):
        self.__monitor = monitor
        self.__resolver = resolver
        self.__widget = widget

    def start(self) -> None:
        screenshot = self.__monitor.screenshot()
        game_context = GameContext()
        tesseract = TesseractOcr()

        # 1. extract game context
        extract_game_context_data_task = ExtractGameContextDataTask(self.__resolver, self.__widget, tesseract)
        self.__resolver.queue(extract_game_context_data_task)

        self.__resolver.resolve(game_context, screenshot)

        # 2. auto healing
        healing_task = HealingTask(self.__resolver)
        self.__resolver.queue(healing_task)

        # 3. auto attacking
        attack_task = AttackTask(self.__resolver)
        self.__resolver.queue(attack_task)

        # 4. auto looting

        self.__resolver.resolve(game_context, screenshot)
