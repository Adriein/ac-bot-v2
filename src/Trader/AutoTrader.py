from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer, Monitor
from src.SharedPackage import GameContext
from src.TaskPackage import TaskResolver, OpenMarketTask, EatTask


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

            Logger.debug('Queuing OpenMarketTask')
            open_depot = OpenMarketTask(self.__widget, player)
            self.__task_resolver.queue(open_depot)

            self.__task_resolver.resolve(game_context, frame)

            raise KeyboardInterrupt

