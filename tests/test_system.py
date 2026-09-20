"""
End-to-End System Integration Checks
"""
import unittest
from app import app

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_frontend_assets(self):
        r_index = self.client.get("/")
        self.assertEqual(r_index.status_code, 200)
        self.assertIn(b"PhysiCards", r_index.data)
        r_index.close()

        r_js = self.client.get("/vendor/katex/katex.min.js")
        self.assertEqual(r_js.status_code, 200)
        self.assertGreater(len(r_js.data), 100000)
        r_js.close()

        r_css = self.client.get("/vendor/katex/katex.min.css")
        self.assertEqual(r_css.status_code, 200)
        self.assertGreater(len(r_css.data), 10000)
        r_css.close()

        r_font = self.client.get("/vendor/katex/fonts/KaTeX_Main-Regular.woff2")
        self.assertEqual(r_font.status_code, 200)
        self.assertGreater(len(r_font.data), 10000)
        r_font.close()

    def test_decks_and_queue(self):
        r_decks = self.client.get("/api/decks").get_json()
        self.assertTrue(r_decks["success"])
        self.assertGreaterEqual(len(r_decks["decks"]), 7)

        r_queue = self.client.get("/api/study/queue?mode=all").get_json()
        self.assertTrue(r_queue["success"])
        self.assertGreater(len(r_queue["queue"]), 0)

        card = r_queue["queue"][0]
        self.assertIn("interval_previews", card)

        r_stats = self.client.get("/api/stats").get_json()
        self.assertTrue(r_stats["success"])
        self.assertGreaterEqual(r_stats["stats"]["total_cards"], 30)

if __name__ == "__main__":
    unittest.main()
