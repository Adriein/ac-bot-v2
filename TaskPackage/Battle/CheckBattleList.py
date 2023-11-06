from TaskPackage.Task import Task


class CheckBattleList(Task):
    def __new__(cls):
        cls.__succeed = False
        cls.__completed = False

    def execute(self) -> None:
        pass

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed
