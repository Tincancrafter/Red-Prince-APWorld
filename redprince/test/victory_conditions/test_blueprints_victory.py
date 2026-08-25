from BaseClasses import CollectionState, Location
from ...options import GoalType
from ...test import RedPrinceTestBase
from ...data_rooms import rooms, core_rooms
from ...constants import *

class TestBlueprintsVictory(RedPrinceTestBase):
    options = {
        "room_draft_sanity": True,
        "item_sanity": True,
        "trophy_sanity": True,
        "goal_type": GoalType.option_blueprints,
    }