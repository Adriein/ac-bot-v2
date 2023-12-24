from abc import ABC, abstractmethod

import numpy as np

from src.SharedPackage import GameContext


class Task(ABC):
    def __init__(self,):
        self.__succeed = False
        self.__completed = False

    @abstractmethod
    def execute(self, context: GameContext, frame: np.ndarray) -> GameContext:
        pass

    @abstractmethod
    def completed(self) -> bool:
        pass

    @abstractmethod
    def succeed(self) -> bool:
        pass

    def success(self) -> None:
        self.__completed = True
        self.__succeed = True

    def fail(self) -> None:
        self.__completed = True
        self.__succeed = False
