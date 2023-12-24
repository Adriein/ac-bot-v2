from src.LoggerPackage import Logger
from src.OperatingSystemPackage import Kernel, Monitor


class TibiaAcBot:
    __monitor = None

    def __init__(self):
        self.setup_global()

    @staticmethod
    def init() -> None:
        try:
            Logger.info('Started...')
            Logger.info('Press Ctrl+C to stop the execution')

            ac_bot_v2 = TibiaAcBot()

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
