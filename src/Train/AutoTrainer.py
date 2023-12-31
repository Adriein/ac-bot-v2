from src.GamePackage import Player, Script
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer, Monitor, Keyboard
from src.SharedPackage import GameContext
from src.TaskPackage import TaskResolver, ExtractHealthDataTask, ExtractManaDataTask, HealingTask, UseManaSurplusTask, \
    EatTask
from src.VendorPackage import TesseractOcr


class AutoTrainer:
    def __init__(
            self,
            monitor: Monitor,
            keyboard: Keyboard,
            task_resolver: TaskResolver,
            widget: GlobalGameWidgetContainer,
            tesseract: TesseractOcr
    ):
        self.__monitor = monitor
        self.__keyboard = keyboard
        self.__task_resolver = task_resolver
        self.__widget = widget
        self.__tesseract = tesseract

    def start(self, game_context: GameContext, player: Player) -> None:
        Logger.info("Starting AutoTrainer")

        while True:
            frame = self.__monitor.screenshot()

            Logger.debug('Queuing ExtractHealthDataTask')
            extract_health_task = ExtractHealthDataTask(self.__widget, self.__tesseract)
            self.__task_resolver.queue(extract_health_task)

            Logger.debug('Queuing ExtractManaDataTask')
            extract_mana_task = ExtractManaDataTask(self.__widget, self.__tesseract)
            self.__task_resolver.queue(extract_mana_task)

            self.__task_resolver.resolve(game_context, frame)

            Logger.debug('Queuing HealingTask')
            healing_task = HealingTask(player)
            self.__task_resolver.queue(healing_task)

            Logger.debug('Queuing UseManaSurplusTask')
            use_mana_surplus_task = UseManaSurplusTask(player)
            self.__task_resolver.queue(use_mana_surplus_task)

            Logger.debug('Queuing EatTask')
            eat_task = EatTask(player)
            self.__task_resolver.queue(eat_task)

            self.__task_resolver.resolve(game_context, frame)
