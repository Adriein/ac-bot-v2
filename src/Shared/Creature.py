from src.Shared.Coordinate import Coordinate


class Creature:
    def __init__(self, name: str, runner: bool, has_to_loot: bool, battle_list_position: list[Coordinate]):
        self.name = name
        self.runner = runner
        self.has_to_loot = has_to_loot
        self.battle_list_position = battle_list_position

    def __str__(self):
        return f'Creature(name={self.name}, runner={self.runner}, has_to_loot={self.has_to_loot}, battle_list_position={self.battle_list_position})'
