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

    def succeed(self) -> bool:
        return self.__succeed

    def completed(self) -> bool:
        return self.__completed

    @abstractmethod
    def __str__(self) -> str:
        pass

    def success(self) -> None:
        self.__completed = True
        self.__succeed = True

    def fail(self) -> None:
        self.__completed = True
        self.__succeed = False
