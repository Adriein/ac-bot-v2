class GameContext:
    def __new__(cls, health: int, mana: int, being_attacked: bool, attacking_creature: bool):
        cls.__health = health
        cls.__mana = mana
        cls.__being_attacked = being_attacked
        cls.__attacking_creature = attacking_creature

    def health(self) -> int:
        return self.__health

    def mana(self) -> int:
        return self.__mana

    def being_attacked(self) -> int:
        return self.__being_attacked

    def attacking_creature(self) -> int:
        return self.__attacking_creature
