import queue

import numpy as np

from src.SharedPackage import GameContext
from src.TaskPackage.Task import Task


class TaskResolver:
    def __init__(self,):
        self.__queue = queue.Queue()

    def resolve(self, game_context: GameContext, frame: np.ndarray, ) -> None:
        while not self.__queue.empty():
            task = self.dequeue()
            print(task)
            print(game_context)
            game_context = task.execute(game_context, frame)

    def queue(self, task: Task) -> None:
        self.__queue.put(task)

    def dequeue(self) -> 'Task':
        return self.__queue.get()
