"""
Integration tests for PhysiCards Flask API.
"""
import json
import os
import shutil
import tempfile
import unittest

import app as app_module
from core.gemini_service import GeminiTutorService
from core.storage import Storage

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_api_cards.db")
        self.storage = Storage(db_path=self.db_path)
        self.service = GeminiTutorService(self.storage)

        self._orig_storage = app_module.storage
        self._orig_service = app_module.gemini_service
        app_module.storage = self.storage
        app_module.gemini_service = self.service
        self.client = app_module.app.test_client()

    def tearDown(self):
        app_module.storage = self._orig_storage
        app_module.gemini_service = self._orig_service
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_decks(self):
        res = self.client.get("/api/decks")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["decks"]), 6)

    def test_get_cards(self):
        res = self.client.get("/api/cards")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["cards"]), 30)

    def test_study_queue_and_review(self):
        # Fetch study queue
        res = self.client.get("/api/study/queue?mode=all&limit=5")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreater(len(data["queue"]), 0)

        card = data["queue"][0]
        card_id = card["id"]

        # Submit review
        review_payload = {
            "card_id": card_id,
            "rating": 3,
            "response_time_ms": 2500
        }
        rev_res = self.client.post("/api/study/review", json=review_payload)
        self.assertEqual(rev_res.status_code, 200)
        rev_data = rev_res.get_json()
        self.assertTrue(rev_data["success"])
        self.assertEqual(rev_data["review"]["card_id"], card_id)

    def test_update_card_physical_meaning(self):
        # Fetch an existing card
        cards_res = self.client.get("/api/cards").get_json()
        self.assertTrue(cards_res["success"])
        card = cards_res["cards"][0]
        card_id = card["id"]

        new_meaning = "Aktualisierte physikalische Intuition: Test erfolgreich!"
        new_validity = "Gültig für beliebige nicht-relativistische Systeme."
        update_payload = {
            "deck_id": card["deck_id"],
            "title": card["title"],
            "front": card["front"],
            "back": card["back"],
            "physical_meaning": new_meaning,
            "validity_domain": new_validity
        }
        put_res = self.client.put(f"/api/cards/{card_id}", json=update_payload)
        self.assertEqual(put_res.status_code, 200)
        put_data = put_res.get_json()
        self.assertTrue(put_data["success"])
        self.assertEqual(put_data["card"]["physical_meaning"], new_meaning)
        self.assertEqual(put_data["card"]["validity_domain"], new_validity)

        # Verify reading fresh returns updated values
        get_res = self.client.get(f"/api/cards/{card_id}")
        self.assertEqual(get_res.status_code, 200)
        get_data = get_res.get_json()
        self.assertEqual(get_data["card"]["physical_meaning"], new_meaning)
        self.assertEqual(get_data["card"]["validity_domain"], new_validity)

    def test_update_deck_api(self):
        # Create a temp deck
        post_res = self.client.post("/api/decks", json={
            "name": "API Deck Test",
            "description": "API Deck Desc",
            "icon": "zap",
            "color": "#3b82f6"
        })
        self.assertEqual(post_res.status_code, 201)
        deck_id = post_res.get_json()["deck"]["id"]

        # Update it
        put_res = self.client.put(f"/api/decks/{deck_id}", json={
            "name": "API Deck Renamed",
            "color": "#ec4899",
            "icon": "sigma",
            "description": "Neue Beschreibung"
        })
        self.assertEqual(put_res.status_code, 200)
        updated = put_res.get_json()["deck"]
        self.assertEqual(updated["name"], "API Deck Renamed")
        self.assertEqual(updated["color"], "#ec4899")
        self.assertEqual(updated["icon"], "sigma")
        self.assertEqual(updated["description"], "Neue Beschreibung")

        # Clean up
        del_res = self.client.delete(f"/api/decks/{deck_id}")
        self.assertEqual(del_res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
