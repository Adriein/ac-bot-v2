from typing import Dict, Generic, TypeVar

T = TypeVar("T")

class GenericMapCollection(Generic[T]):
    def __init__(self, arg: list[T] | None = None):
        if arg is None:
            self.dic: Dict[str | int, T] = dict()
            return

        self.dic: Dict[str | int, T] = dict(arg)

    def has(self, key: str | int) -> bool:
        return key in self.dic

    def get(self, key: str | int) -> T | None:
        return self.dic.get(key)

    def set(self, key: str | int, value: T) -> None:
        self.dic[key] = value

    def __str__(self) -> str:
        return str(self.dic)