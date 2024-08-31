from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer, Monitor
from src.SharedPackage import GameContext
from src.TaskPackage import TaskResolver, UseManaSurplusTask, EatTask

class AutoTrader:
    def __init__(
            self,
            monitor: Monitor,
            task_resolver: TaskResolver,
            widget: GlobalGameWidgetContainer
    ):
        self.__monitor = monitor
        self.__task_resolver = task_resolver
        self.__widget = widget

    def start(self, game_context: GameContext, player: Player) -> None:
        Logger.info("Starting AutoTrader")

        while True:
            frame = self.__monitor.screenshot()

            Logger.debug('Queuing UseManaSurplusTask')
            use_mana_surplus_task = UseManaSurplusTask(player)
            self.__task_resolver.queue(use_mana_surplus_task)

            Logger.debug('Queuing EatTask')
            eat_task = EatTask(player)
            self.__task_resolver.queue(eat_task)

            self.__task_resolver.resolve(game_context, frame)

