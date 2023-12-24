from src.LoggerPackage import Logger
from src.OperatingSystemPackage import Kernel, Monitor, GlobalGameWidgetContainer
from src.SharedPackage import PyAutoGui
from src.Cavebot import CaveBot
from src.TaskPackage import TaskResolver


class TibiaAcBot:
    def __init__(self):
        self.__monitor = None
        self.__global_widget_container = None
        self.__task_resolver = None

        self.setup_global()

    def init(self,) -> None:
        try:
            Logger.info('Started...')
            Logger.info('Press Ctrl+C to stop the execution')

            cavebot = CaveBot(self.__monitor, self.__task_resolver)

            cavebot.start()

        except KeyboardInterrupt:
            Logger.info('Graceful shutdown')
            raise SystemExit
        except Exception as error:
            Logger.error(str(error), error)
            raise SystemExit from error

    def setup_global(self) -> None:
        Logger.info('Creating Kernel...')
        os_kernel = Kernel()

        Logger.info('Creating Monitor...')
        self.__monitor = Monitor(os_kernel)

        Logger.info('Locating widgets in the screen...')
        self.__global_widget_container = GlobalGameWidgetContainer(self.__monitor, PyAutoGui())

        Logger.info('Initialize TaskResolver...')
        self.__task_resolver = TaskResolver()

    def initialize_dependencies(self):
        pass


TibiaAcBot().init()

'''
1. enemies in the battle list?
2. attack
3. need healing?
4. heal
'''

'''
first check status of the game and queue taks with prio
then resolve the tasks and loop again
'''
