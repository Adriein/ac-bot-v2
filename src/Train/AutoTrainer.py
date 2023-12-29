from src.LoggerPackage import Logger
from src.OperatingSystemPackage import GlobalGameWidgetContainer, Monitor
from src.TaskPackage import TaskResolver, ExtractHealthDataTask, ExtractManaDataTask
from src.SharedPackage import GameContext
from src.VendorPackage import TesseractOcr


class AutoTrainer:
    def __init__(self, monitor: Monitor, task_resolver: TaskResolver, widget: GlobalGameWidgetContainer):
        self.__monitor = monitor
        self.__task_resolver = task_resolver
        self.__widget = widget

    def start(self) -> None:
        Logger.info("Starting AutoTrainer")

        tesseract = TesseractOcr()
        game_context = GameContext()

        while True:
            frame = self.__monitor.screenshot()

            Logger.debug('Queuing ExtractHealthDataTask')
            extract_health_task = ExtractHealthDataTask(self.__widget, tesseract)
            self.__task_resolver.queue(extract_health_task)

            Logger.debug('Queuing ExtractManaDataTask')
            extract_mana_task = ExtractManaDataTask(self.__widget, tesseract)
            self.__task_resolver.queue(extract_mana_task)

            self.__task_resolver.resolve(game_context, frame)


            # 1.Collect relevant screen info
            # 2.Execute relevant tasks
