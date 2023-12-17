from src.TaskPackage import ExtractGameContextDataTask
from src.TaskPackage import TaskResolver


class CaveBot:

    def __new__(cls, resolver: TaskResolver):
        cls.__resolver = resolver

    def init(self) -> None:
        # 1. extract game context
        extract_game_context_data_task = ExtractGameContextDataTask(self.__resolver)
        self.__resolver.queue(extract_game_context_data_task)

        # 2. auto healing

        # 3. auto attacking

        # 4. auto looting

        self.__resolver.resolve()
