"""
Unit tests for SM-2 Spaced Repetition logic.
"""

import unittest

from core.models import ReviewState
from core.sm2 import calculate_sm2, predict_intervals


class TestSM2(unittest.TestCase):
    def test_initial_review_good(self):
        state = ReviewState(
            card_id="c1", repetitions=0, interval_days=0.0, ease_factor=2.5
        )
        new_state, interval = calculate_sm2(state, rating=3)  # Good
        self.assertEqual(new_state.repetitions, 1)
        self.assertEqual(interval, 1.0)
        self.assertGreaterEqual(new_state.ease_factor, 1.3)

    def test_initial_review_easy(self):
        state = ReviewState(
            card_id="c1", repetitions=0, interval_days=0.0, ease_factor=2.5
        )
        new_state, interval = calculate_sm2(state, rating=4)  # Easy
        self.assertEqual(new_state.repetitions, 1)
        self.assertEqual(interval, 3.0)
        self.assertGreater(new_state.ease_factor, 2.5)

    def test_second_review_good(self):
        state = ReviewState(
            card_id="c1", repetitions=1, interval_days=1.0, ease_factor=2.5
        )
        new_state, interval = calculate_sm2(state, rating=3)
        self.assertEqual(new_state.repetitions, 2)
        self.assertEqual(interval, 6.0)

    def test_lapse_resets_repetitions(self):
        state = ReviewState(
            card_id="c1", repetitions=5, interval_days=30.0, ease_factor=2.6, lapses=0
        )
        new_state, interval = calculate_sm2(state, rating=1)  # Failed
        self.assertEqual(new_state.repetitions, 0)
        self.assertEqual(new_state.lapses, 1)
        self.assertLess(interval, 0.1)  # Due again in minutes

    def test_predict_intervals(self):
        state = ReviewState(
            card_id="c1", repetitions=0, interval_days=0.0, ease_factor=2.5
        )
        predictions = predict_intervals(state)
        self.assertIn(1, predictions)
        self.assertIn(2, predictions)
        self.assertIn(3, predictions)
        self.assertIn(4, predictions)
        self.assertIn("Min", predictions[1])


if __name__ == "__main__":
    unittest.main()
