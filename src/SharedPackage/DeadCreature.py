from .Creature import Creature
from .Waypoint import Waypoint


class DeadCreature:
    def __init__(self, creature: Creature, position: Waypoint):
        self.__creature = creature
        self.__position = position

    def is_runner(self) -> bool:
        return self.__creature.is_runner()

    def has_to_loot(self) -> bool:
        return self.__creature.has_to_loot()
