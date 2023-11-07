from src.LoggerPackage import Logger


class TibiaAcBot:
    @staticmethod
    def init():
        try:
            TibiaAcBot.setup_global()

            Logger.info('Started...')
            Logger.info('Press Ctrl+C to stop the execution')

        except KeyboardInterrupt:
            Logger.info('Graceful shutdown')
            raise SystemExit
        except Exception as error:
            Logger.error(str(error), error)
            raise SystemExit from error

    @staticmethod
    def setup_global() -> None:
        Logger.info('Setting env...')


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
