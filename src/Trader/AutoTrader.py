from src.GamePackage import Player
from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer, Monitor
from src.SharedPackage import GameContext, ManualIterationInterrupt
from src.TaskPackage import TaskResolver, OpenMarketTask, SearchItemInMarket, SelectItemInMarket, ExtractSelectedItemInfo, NotifyItemInfo, CancelItemSearch
from src.VendorPackage import PyAutoGui


class AutoTrader:
    def __init__(
            self,
            monitor: Monitor,
            task_resolver: TaskResolver,
            widget: GlobalGameWidgetContainer,
            pyautogui: PyAutoGui,
    ):
        self.__monitor = monitor
        self.__task_resolver = task_resolver
        self.__widget = widget
        self.__pyautogui = pyautogui

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
                self.__task_resolver.resolve(game_context, frame)

                Logger.debug('Queuing SearchItemInMarketTask')
                search_item = SearchItemInMarket(self.__widget, player)
                self.__task_resolver.queue(search_item)

                Logger.debug('Queuing SelectItemInMarket')
                select_item = SelectItemInMarket(self.__widget, player)
                self.__task_resolver.queue(select_item)

                Logger.debug('Queuing ExtractSelectedItemInfo')
                extract_selected_item_info = ExtractSelectedItemInfo(self.__widget, self.__pyautogui)
                self.__task_resolver.queue(extract_selected_item_info)

                Logger.debug('Queuing NotifyItemInfo')
                notify_item_info = NotifyItemInfo(self.__widget)
                self.__task_resolver.queue(notify_item_info)

                Logger.debug('Queuing CancelItemSearch')
                cancel_item_search = CancelItemSearch(self.__widget, player)
                self.__task_resolver.queue(cancel_item_search)

                self.__task_resolver.resolve(game_context, frame)

            except ManualIterationInterrupt:
                continue
