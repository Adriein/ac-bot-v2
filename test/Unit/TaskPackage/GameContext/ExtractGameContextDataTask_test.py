from pytest_mock import MockerFixture

from src.TaskPackage import (
    ExtractGameContextDataTask,
    TaskResolver,
    GameContext,
    ExtractBattleListDataTask,
    ExtractHealthDataTask,
    ExtractManaDataTask
)


class TestExtractGameContextDataTask:

    def test_should_queue_into_task_resolver_3_actions(self, mocker: MockerFixture):
        game_context = GameContext()
        task_resolver = TaskResolver(game_context)

        mocked_task_resolver_queue_function = mocker.spy(task_resolver, 'queue')

        extract_game_context_data_task = ExtractGameContextDataTask(task_resolver)

        extract_game_context_data_task.execute(game_context)

        assert mocked_task_resolver_queue_function.call_count == 3

    def test_should_queue_into_task_resolver_the_correct_tasks(self,):
        game_context = GameContext()
        task_resolver = TaskResolver(game_context)

        extract_game_context_data_task = ExtractGameContextDataTask(task_resolver)

        extract_game_context_data_task.execute(game_context)

        extract_mana_data_task = task_resolver.dequeue()
        extract_health_data_task = task_resolver.dequeue()
        extract_battle_list_data_task = task_resolver.dequeue()

        assert isinstance(extract_mana_data_task, ExtractBattleListDataTask)
        assert isinstance(extract_health_data_task, ExtractHealthDataTask)
        assert isinstance(extract_battle_list_data_task, ExtractManaDataTask)
