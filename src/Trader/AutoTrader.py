from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer, Monitor
from src.SharedPackage import GameContext, ManualIterationInterrupt
from src.TaskPackage import TaskResolver, OpenMarketTask, SearchItemInMarket, SelectItemInMarket


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
            try:
                frame = self.__monitor.screenshot()

                # Logger.debug('Queuing OpenDepotTask')
                # open_depot = OpenDepotTask(self.__widget, player)
                # self.__task_resolver.queue(open_depot)

                Logger.debug('Queuing OpenMarketTask')
                open_market = OpenMarketTask(self.__widget, player)
                self.__task_resolver.queue(open_market)

                Logger.debug('Queuing SearchItemInMarketTask')
                search_item = SearchItemInMarket(self.__widget, player)
                self.__task_resolver.queue(search_item)

                Logger.debug('Queuing SelectItemInMarket')
                select_item = SelectItemInMarket(self.__widget, player)
                self.__task_resolver.queue(select_item)

                self.__task_resolver.resolve(game_context, frame)

                raise KeyboardInterrupt

            except ManualIterationInterrupt:
                continue

