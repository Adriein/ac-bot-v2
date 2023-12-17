from abc import ABC, abstractmethod
from src.TaskPackage.GameContext.GameContext import GameContext


class Task(ABC):
    @abstractmethod
    def execute(self, context: GameContext) -> GameContext:
        pass

    @abstractmethod
    def completed(self) -> bool:
        pass

    @abstractmethod
    def succeed(self) -> bool:
        pass
