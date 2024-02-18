from src.GamePackage import Player, Script, Map
from src.OperatingSystemPackage import Monitor, GlobalGameWidgetContainer
from src.SharedPackage import GameContext
from src.TaskPackage import TaskResolver, ExtractGameContextDataTask, AttackTask, HealingTask, LootTask, EatTask, SmartSpellHealingTask, LocationTask, WalkTask, ResolveWaypointActionTask
from src.VendorPackage import TesseractOcr, PyAutoGui


class CaveBot:

    def __init__(
            self,
            monitor: Monitor,
            resolver: TaskResolver,
            widget: GlobalGameWidgetContainer,
            tesseract: TesseractOcr,
            game_map: Map
    ):
        self.__monitor = monitor
        self.__resolver = resolver
        self.__widget = widget
        self.__tesseract = tesseract
        self.__game_map = game_map

    def start(self, game_context: GameContext, player: Player) -> None:
        while True:
            screenshot = self.__monitor.screenshot()

            # 1. extract game context
            extract_game_context_data_task = ExtractGameContextDataTask(self.__resolver, self.__widget, self.__tesseract)
            #self.__resolver.queue(extract_game_context_data_task)

            #self.__resolver.resolve(game_context, screenshot)

            # 2. auto healing
            healing_task = HealingTask(player)
            #self.__resolver.queue(healing_task)

            # 3. auto attacking
            attack_task = AttackTask(player)
            #self.__resolver.queue(attack_task)

            # 4. auto looting
            loot_task = LootTask(player, self.__widget)
            #self.__resolver.queue(loot_task)

            # 5. waste mana
            spell_healing_task = SmartSpellHealingTask(player)
            #self.__resolver.queue(spell_healing_task)

            # 6. Eat food
            eat_task = EatTask(player)
            #self.__resolver.queue(eat_task)

            #self.__resolver.resolve(game_context, screenshot)

            # 8. Locate player position
            location_task = LocationTask(self.__game_map)
            self.__resolver.queue(location_task)

            # 8. Walk
            walk_task = WalkTask(self.__game_map, player)
            self.__resolver.queue(walk_task)

            # 9. Resolve waypoint
            resolve_waypoint_task = ResolveWaypointActionTask(self.__game_map, player, self.__widget)
            self.__resolver.queue(resolve_waypoint_task)

            self.__resolver.resolve(game_context, screenshot)
