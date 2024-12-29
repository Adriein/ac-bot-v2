from src.GamePackage import Player, Map
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer, Monitor
from src.SharedPackage import GameContext
from src.TaskPackage import TaskResolver, UseManaSurplusTask, EatTask, SecurityTrainingFloorCheckTask
from src.VendorPackage import TesseractOcr


class AutoTrainer:
    def __init__(
            self,
            monitor: Monitor,
            task_resolver: TaskResolver,
            widget: GlobalGameWidgetContainer,
            tesseract: TesseractOcr,
            game_map: Map
    ):
        self.__monitor = monitor
        self.__task_resolver = task_resolver
        self.__widget = widget
        self.__tesseract = tesseract
        self.__game_map = game_map

    def start(self, game_context: GameContext, player: Player) -> None:
        Logger.info("Starting AutoTrainer")

        while True:
            frame = self.__monitor.screenshot()

            Logger.debug('Queuing SecurityTrainingFloorCheckTask')
            security_lvl_check = SecurityTrainingFloorCheckTask(self.__game_map, self.__monitor)
            self.__task_resolver.queue(security_lvl_check)

            Logger.debug('Queuing UseManaSurplusTask')
            use_mana_surplus_task = UseManaSurplusTask(player)
            self.__task_resolver.queue(use_mana_surplus_task)

            Logger.debug('Queuing EatTask')
            eat_task = EatTask(player)
            self.__task_resolver.queue(eat_task)

            self.__task_resolver.resolve(game_context, frame)
