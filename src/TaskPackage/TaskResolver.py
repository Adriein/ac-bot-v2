import queue
from src.TaskPackage.GameContext import GameContext
from src.TaskPackage.Task import Task


class TaskResolver:
    def __new__(cls):
        cls.__queue = queue.Queue()

    def resolve(self, game_context: GameContext) -> None:
        while not self.__queue.empty():
            task = self.dequeue()

            game_context = task.execute(game_context)

    def queue(self, task: Task) -> None:
        self.__queue.put(task)

    def dequeue(self) -> 'Task':
        return self.__queue.get()
