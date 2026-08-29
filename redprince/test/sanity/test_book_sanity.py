from .. import RedPrinceTestBase
from ...data_other_locations import bookshop_items, library_checkouts


class TestBookSanityDisabled(RedPrinceTestBase):
    options = {
        "bookshop_sanity": False,
        "library_checkout_sanity": False,
    }

    def test_book_locations_are_disabled_by_default(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertTrue(location_names.isdisjoint(bookshop_items))
        self.assertTrue(location_names.isdisjoint(library_checkouts))


class TestBookSanityEnabled(RedPrinceTestBase):
    options = {
        "bookshop_sanity": True,
        "library_checkout_sanity": True,
    }

    def test_all_book_locations_are_created(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        self.assertTrue(set(bookshop_items).issubset(location_names))
        self.assertTrue(set(library_checkouts).issubset(location_names))
        self.assertEqual(6, len(bookshop_items))
        self.assertEqual(12, len(library_checkouts))
