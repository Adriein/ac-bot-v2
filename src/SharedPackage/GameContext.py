from .Creature import Creature
from .Waypoint import Waypoint
from .MarketItem import MarketItem
from datetime import datetime
from copy import deepcopy
from src.UtilPackage import Time, LinkedList


class GameContext:
    @staticmethod
    def copy(game_context: 'GameContext') -> 'GameContext':
        return deepcopy(game_context)

    def __str__(self):
        return f"GameContext"

    def __init__(self):
        self.__health = 0
        self.__mana = 0

        self.__last_meal_time = Time.now()
        self.__next_meal_time = Time.now()

        self.__is_attacking = False

        self.__creatures_in_range = list()
        self.__script_enemies = list()

        self.__dead_creature = None

        self.__current_waypoint = None
        self.__current_floor = None
        self.__cave_route = None
        self.__combat_stance = None
        self.__attacking_creature = None
        self.__start_attacking = Time.now()

        self.__has_to_wear_ring = False
        self.__is_ring_equipped = False

        self.__trade_items = list()
        self.__is_market_open = False
        self.__is_item_searched = False
        self.__is_item_selected = False
        self.__is_scrapping_item_info = False
        self.__scrapped_item = None

    def set_health(self, health: int) -> None:
        self.__health = health

    def get_health(self) -> int:
        return self.__health

    def set_mana(self, mana: int) -> None:
        self.__mana = mana

    def get_mana(self) -> int:
        return self.__mana

    def set_is_attacking(self, is_attacking: bool) -> None:
        self.__is_attacking = is_attacking

    def get_is_attacking(self) -> bool:
        return self.__is_attacking

    def set_attacking_creature(self, creature: Creature) -> None:
        self.__attacking_creature = creature

    def get_attacking_creature(self) -> Creature:
        return self.__attacking_creature

    def set_start_attacking(self, date: datetime) -> None:
        self.__start_attacking = date

    def get_start_attacking(self) -> datetime:
        return self.__start_attacking

    def set_creatures_in_range(self, creatures: list[Creature]) -> None:
        self.__creatures_in_range = creatures

    def get_creatures_in_range(self) -> list[Creature]:
        return self.__creatures_in_range

    def set_script_enemies(self, enemies: list[Creature]) -> None:
        self.__script_enemies = enemies

    def get_script_enemies(self) -> list[Creature]:
        return self.__script_enemies

    def set_last_meal_time(self, meal_time: datetime) -> None:
        self.__last_meal_time = meal_time

    def get_last_meal_time(self) -> datetime:
        return self.__last_meal_time

    def set_next_meal_time(self, meal_time: datetime) -> None:
        self.__next_meal_time = meal_time

    def get_next_meal_time(self) -> datetime:
        return self.__next_meal_time

    def get_dead_creature(self) -> Creature:
        return self.__dead_creature

    def set_dead_creature(self, creature: Creature | None) -> None:
        self.__dead_creature = creature

    def set_current_waypoint(self, waypoint: Waypoint) -> None:
        self.__current_waypoint = waypoint

    def get_current_waypoint(self) -> Waypoint:
        return self.__current_waypoint

    def set_current_floor(self, floor: int) -> None:
        self.__current_floor = floor

    def get_current_floor(self) -> int:
        return self.__current_floor

    def set_cave_route(self, route: LinkedList[Waypoint]) -> None:
        initial_waypoint = route.head.data

        self.set_current_floor(initial_waypoint.z)
        self.set_current_waypoint(initial_waypoint)

        self.__cave_route = route

    def get_cave_route(self) -> LinkedList[Waypoint]:
        return self.__cave_route

    def has_creatures_in_range(self) -> bool:
        return len(self.__creatures_in_range) > 0

    def set_combat_stance(self, combat_stance: str) -> None:
        self.__combat_stance = combat_stance

    def get_combat_stance(self) -> str:
        return self.__combat_stance

    def set_has_to_wear_ring(self, has_to_wear_ring: bool) -> None:
        self.__has_to_wear_ring = has_to_wear_ring

    def get_has_to_wear_ring(self) -> bool:
        return self.__has_to_wear_ring

    def get_is_ring_equipped(self) -> bool:
        return self.__is_ring_equipped

    def set_is_ring_equipped(self, is_equipped: bool) -> None:
        self.__is_ring_equipped = is_equipped

    def get_is_market_open(self) -> bool:
        return self.__is_market_open

    def set_is_market_open(self, is_market_open: bool) -> None:
        self.__is_market_open = is_market_open

    def get_is_item_searched(self) -> bool:
        return self.__is_item_searched

    def set_is_item_searched(self, is_item_searched: bool) -> None:
        self.__is_item_searched = is_item_searched

    def get_is_item_selected(self) -> bool:
        return self.__is_item_selected

    def set_is_item_selected(self, is_item_selected: bool) -> None:
        self.__is_item_selected = is_item_selected

    def get_is_scrapping_item_info(self) -> bool:
        return self.__is_scrapping_item_info

    def set_is_scrapping_item_info(self, is_scrapping_item_info: bool) -> None:
        self.__is_scrapping_item_info = is_scrapping_item_info

    def get_scrapped_item(self) -> MarketItem:
        return self.__scrapped_item

    def set_scrapped_item(self, scrapped_item: MarketItem | None) -> None:
        self.__scrapped_item = scrapped_item

    def get_trade_items(self) -> list[str]:
        return self.__trade_items

    def set_trade_items(self, items: list[str]) -> None:
        self.__trade_items = items
