from .Task import Task
from .TaskResolver import TaskResolver

from .GameContext.ExtractGameContextDataTask import ExtractGameContextDataTask
from .GameContext.Battle.ExtractBattleListDataTask import ExtractBattleListDataTask
from .GameContext.Battle.ExtractAttackStatusBattleListTask import ExtractAttackStatusBattleListTask
from .GameContext.ExtractGameContextDataTask import ExtractManaDataTask
from .GameContext.ExtractGameContextDataTask import ExtractHealthDataTask

from .GameActions.AttackTask import AttackTask
from .GameActions.HealingTask import HealingTask
from .GameActions.UseManaSurplusTask import UseManaSurplusTask
from .GameActions.EatTask import EatTask
from .GameActions.LootTask import LootTask
from .GameActions.SmartSpellHealingTask import SmartSpellHealingTask
