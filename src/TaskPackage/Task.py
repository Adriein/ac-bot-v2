from abc import ABC, abstractmethod


class Task(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def completed(self) -> bool:
        pass

    @abstractmethod
    def succeed(self) -> bool:
        pass
