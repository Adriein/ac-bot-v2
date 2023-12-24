from src.OperatingSystemPackage import Monitor
from src.TaskPackage import TaskResolver, ExtractGameContextDataTask, AttackTask, HealingTask


class CaveBot:

    def __init__(self, monitor: Monitor, resolver: TaskResolver):
        self.__monitor = monitor
        self.__resolver = resolver

    def init(self) -> None:
        screenshot = self.__monitor.screenshot()

        # 1. extract game context
        extract_game_context_data_task = ExtractGameContextDataTask(self.__resolver)
        self.__resolver.queue(extract_game_context_data_task)

        # 2. auto healing
        healing_task = HealingTask(self.__resolver)
        self.__resolver.queue(healing_task)

        # 3. auto attacking
        attack_task = AttackTask(self.__resolver)
        self.__resolver.queue(attack_task)

        # 4. auto looting

        self.__resolver.resolve()
