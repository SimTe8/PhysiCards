"""
Unit tests for SQLite storage layer.
"""

import os
import tempfile
import unittest

from core.models import Card, Deck
from core.storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_cards.db")
        self.storage = Storage(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_default_seeding(self):
        decks = self.storage.get_decks()
        self.assertGreaterEqual(len(decks), 6)
        cards = self.storage.get_cards()
        self.assertGreaterEqual(len(cards), 30)

    def test_create_and_delete_deck(self):
        new_deck = Deck(id="test_deck", name="Test Deck", description="Testing")
        self.storage.create_deck(new_deck)
        d = self.storage.get_deck("test_deck")
        self.assertIsNotNone(d)
        self.assertEqual(d["name"], "Test Deck")

        # Test updating deck
        updated = self.storage.update_deck(
            "test_deck",
            {
                "name": "Updated Test Deck",
                "color": "#6366f1",
                "icon": "sigma",
                "description": "Updated Description",
            },
        )
        self.assertEqual(updated["name"], "Updated Test Deck")
        self.assertEqual(updated["color"], "#6366f1")
        self.assertEqual(updated["icon"], "sigma")
        self.assertEqual(updated["description"], "Updated Description")

        self.storage.delete_deck("test_deck")
        self.assertIsNone(self.storage.get_deck("test_deck"))

    def test_reine_mathematik_deck_seeded(self):
        d = self.storage.get_deck("reine_mathematik")
        self.assertIsNotNone(d)
        self.assertEqual(d["name"], "Reine Mathematik & Analysis")
        math_cards = self.storage.get_cards(deck_id="reine_mathematik")
        self.assertGreaterEqual(len(math_cards), 10)
        # Check specific card
        l2_card = self.storage.get_card("math_l2_space_definition")
        self.assertIsNotNone(l2_card)
        self.assertIn("L^2", l2_card["title"])

    def test_create_and_review_card(self):
        card = Card(
            id="test_card_1",
            deck_id="elektrodynamik",
            title="Coulomb-Gesetz",
            front="Wie lautet das Coulomb-Gesetz?",
            back=r"$$F = \frac{1}{4\pi\varepsilon_0} \frac{q_1 q_2}{r^2}$$",
        )
        self.storage.create_card(card)
        c = self.storage.get_card("test_card_1")
        self.assertIsNotNone(c)
        self.assertEqual(c["title"], "Coulomb-Gesetz")

        # Record a good review
        rev = self.storage.record_review("test_card_1", rating=3)
        self.assertEqual(rev["state"]["repetitions"], 1)

        c_after = self.storage.get_card("test_card_1")
        self.assertEqual(c_after["repetitions"], 1)

    def test_export_import(self):
        data = self.storage.export_all()
        self.assertIn("decks", data)
        self.assertIn("cards", data)

        # Import into fresh db
        new_db_path = os.path.join(self.temp_dir, "import_test.db")
        new_storage = Storage(db_path=new_db_path)
        d_cnt, c_cnt = new_storage.import_all(data)
        self.assertGreaterEqual(d_cnt, 6)
        self.assertGreaterEqual(c_cnt, 30)
        if os.path.exists(new_db_path):
            os.remove(new_db_path)


if __name__ == "__main__":
    unittest.main()
