import queue
from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task


class TaskResolver:
    def __init__(self, game_context: GameContext):
        self.__queue = queue.Queue()
        self.__game_context = game_context

    def resolve(self, ) -> None:
        game_context = self.__game_context

        while not self.__queue.empty():
            task = self.dequeue()

            game_context = task.execute(game_context)

    def queue(self, task: Task) -> None:
        self.__queue.put(task)

    def dequeue(self) -> 'Task':
        return self.__queue.get()
