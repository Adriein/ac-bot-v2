import queue
from src.TaskPackage.Task import Task


class TaskResolver:
    def __new__(cls):
        cls.__queue = queue.Queue()

    def resolve(self) -> None:
        while not self.__queue.empty():
            task = self.dequeue()

            task.execute()

    def queue(self, task: Task) -> None:
        self.__queue.put(task)

    def dequeue(self) -> 'Task':
        return self.__queue.get()
