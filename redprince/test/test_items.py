from BaseClasses import CollectionState, Location
from ..options import GoalType
from ..test import RedPrinceTestBase
from ..data_rooms import rooms, core_rooms
from ..data_other_locations import upgrade_disks
from ..constants import *
from ..locations import LOCATION_NAME_TO_ID
from ..items import ITEM_NAME_TO_ID

class TestItems(RedPrinceTestBase):
    options = {
        "room_draft_sanity": True,
        "goal_type": GoalType.option_room46,
    }

    def test_all_item_ids_unique(self):
        mem = dict()
        for name, id in ITEM_NAME_TO_ID.items():
            if id in mem:
                self.fail(f"Duplicate item ID {id} for {name} and {mem[id]}")
            mem[id] = name
    
    def test_item_groups(self):
        for name, group in self.world.item_name_groups.items():
            print(f"Group {name} contains: {group}\n")

    def test_blackbridge_satellite_progressive_tiers(self):
        progression_names = [item.name for item in self.multiworld.itempool]
        self.assertEqual(2, progression_names.count("Progressive Blackbridge/Satellite"))
        self.assertNotIn("Blackbridge Grotto", progression_names)
        self.assertNotIn("Satellite Dish", progression_names)

    def test_blackbridge_location_name_matches_client(self):
        self.assertIn("Laboratory Puzzle - Blackbridge", LOCATION_NAME_TO_ID)
        self.assertNotIn("Laboratory Puzzle", LOCATION_NAME_TO_ID)


class TestVanillaUpgradeDisks(RedPrinceTestBase):
    options = {
        "room_draft_sanity": True,
        "upgrade_disk_sanity": False,
        "goal_type": GoalType.option_room46,
    }

    def test_upgrade_disks_are_not_precollected(self):
        precollected_names = {
            item.name for item in self.multiworld.precollected_items[self.player]
        }
        self.assertTrue(
            precollected_names.isdisjoint(upgrade_disks),
            "Vanilla upgrade disks must not be sent to the client as starting items",
        )


class TestCommissaryDiskRequiresShopSanity(RedPrinceTestBase):
    options = {
        "room_draft_sanity": True,
        "upgrade_disk_sanity": True,
        "special_shop_sanity": False,
        "goal_type": GoalType.option_room46,
    }

    def test_commissary_disk_location_and_item_are_omitted(self):
        with self.assertRaises(KeyError):
            self.multiworld.get_location("Upgrade Disk - Commissary", self.player)
        self.assertNotIn(
            "UPGRADE DISK COMMISSARY",
            [item.name for item in self.multiworld.itempool],
        )


class TestCommissaryEconomyLogic(RedPrinceTestBase):
    options = {
        "room_draft_sanity": True,
        "standard_item_sanity": True,
        "upgrade_disk_sanity": True,
        "special_shop_sanity": True,
        "goal_type": GoalType.option_room46,
    }

    def test_commissary_disk_requires_coin_purse(self):
        self.collect_all_but(["COIN PURSE"])
        self.assertFalse(self.can_reach_location("Upgrade Disk - Commissary"))
        self.collect_by_name("COIN PURSE")
        self.assertTrue(self.can_reach_location("Upgrade Disk - Commissary"))
