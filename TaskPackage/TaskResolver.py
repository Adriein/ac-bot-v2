from TaskPackage.Task import Task


class TaskResolver:
    def __new__(cls):
        cls.__queue = list()

    def resolve(self, task: Task) -> None:
        task.execute()

    def queue(self, task: Task) -> None:
        self.__queue.append(task)

    def dequeue(self) -> 'Task':
        return self.__queue.pop()
