from typing import Any


class MapCollection:
    def __init__(self, arg: list | None = None):
        if arg is None:
            self.dic = dict()
            return

        self.dic = dict(arg)

    def has(self, key: str) -> bool:
        return key in self.dic

    def get(self, key: str | int) -> Any | None:
        return self.dic.get(key)

    def set(self, key: str | int, value: Any) -> None:
        self.dic[key] = value
