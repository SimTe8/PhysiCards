import json
import os
import shutil
import tempfile
import unittest

import app as app_module
from core.gemini_service import GeminiTutorService, get_system_prompt
from core.models import Card
from core.storage import Storage


class TestGeminiIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_gemini_cards.db")
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

    def test_settings_storage(self):
        """Verify API key and model settings can be saved and retrieved."""
        self.storage.set_setting("gemini_api_key", "AIzaSyTestKey123456789")
        self.storage.set_setting("gemini_model", "gemini-3.6-flash")
        self.storage.set_setting("gemini_style", "socratic")

        self.assertEqual(self.service.get_api_key(), "AIzaSyTestKey123456789")
        self.assertEqual(self.service.get_model(), "gemini-3.6-flash")
        self.assertEqual(self.service.get_tutor_style(), "socratic")

        # Test GET /api/ai/settings endpoint
        res = self.client.get("/api/ai/settings").get_json()
        self.assertTrue(res["success"])
        self.assertTrue(res["has_key"])
        self.assertTrue(res["masked_key"].startswith("AIzaSy"))
        self.assertTrue(res["masked_key"].endswith("6789"))
        self.assertIn("...", res["masked_key"])
        self.assertIn("available_models", res)
        self.assertTrue(
            any(m["id"] == "gemini-3.6-flash" for m in res["available_models"])
        )
        self.assertTrue(
            any(m["id"] == "gemini-3.1-pro-preview" for m in res["available_models"])
        )

        # Test auto-migration of deprecated models (e.g. gemini-2.5-flash -> gemini-3.6-flash)
        self.storage.set_setting("gemini_model", "gemini-2.5-flash")
        migrated = self.service.get_model()
        self.assertEqual(migrated, "gemini-3.6-flash")

        # Clean up
        self.storage.delete_setting("gemini_api_key")
        self.storage.delete_setting("gemini_model")
        self.storage.delete_setting("gemini_style")

    def test_system_prompt_builder(self):
        """Verify system prompt injects card metadata and LaTeX guidelines."""
        card = Card(
            id="test_card_1",
            deck_id="quantenmechanik",
            title="Schrödinger-Gleichung",
            front="Wie lautet die zeitabhängige Schrödinger-Gleichung?",
            back=r"i\hbar \frac{\partial \psi}{\partial t} = \hat{H}\psi",
            hint="Energieoperator",
            formula_breakdown=r"- $\hat{H}$: Hamilton-Operator",
            physical_meaning="Deterministische unitäre Zeitentwicklung der Wahrscheinlichkeitsamplitude.",
            validity_domain="Nicht-relativistisch",
            tags=["QM", "Schrödinger"],
            difficulty=3,
        )

        prompt_socratic = get_system_prompt(card, style="socratic")
        self.assertIn("Schrödinger-Gleichung", prompt_socratic)
        self.assertIn("Hamilton-Operator", prompt_socratic)
        self.assertIn("sokratisch", prompt_socratic.lower())
        self.assertIn("```json:card", prompt_socratic)

        prompt_intuitive = get_system_prompt(card, style="intuitive")
        self.assertIn("Alltags-Analogien", prompt_intuitive)

    def test_chat_endpoint_without_key(self):
        """Verify chat endpoint returns clear error SSE when no key is set."""
        self.storage.delete_setting("gemini_api_key")
        res = self.client.post("/api/ai/chat", json={"message": "Hallo Tutor"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.mimetype, "text/event-stream")
        data = res.data.decode("utf-8")
        self.assertIn("Kein API-Key hinterlegt", data)
        self.assertIn("[DONE]", data)

    def test_connection_test_failure_without_key(self):
        """Verify test connection fails gracefully if key is absent or invalid."""
        res = self.client.post("/api/ai/test", json={"api_key": ""}).get_json()
        self.assertFalse(res["success"])
        self.assertIn("Kein Google AI Studio API-Key", res["error"])

    def test_card_generator_endpoint_validation(self):
        """Verify generate-card endpoint requires topic."""
        res = self.client.post("/api/ai/generate-card", json={}).get_json()
        self.assertFalse(res["success"])
        self.assertIn("erforderlich", res["error"])

    def test_card_preview_json_format(self):
        """Verify standardized json:card structure matches Card dataclass."""
        mock_raw_ai_text = """Hier ist deine Erklärung zur Compton-Streuung.
```json:card
{
  "deck_id": "quantenmechanik",
  "title": "Compton-Streuung & Wellenlängenverschiebung",
  "front": "Wie lautet die Formel für die Zunahme der Wellenlänge bei der Compton-Streuung?",
  "back": "\\\\Delta \\\\lambda = \\\\lambda' - \\\\lambda = \\\\lambda_C (1 - \\\\cos \\\\theta)",
  "hint": "lambda_C ist die Compton-Wellenlänge des Elektrons",
  "formula_breakdown": "- \\\\lambda_C = \\\\frac{h}{m_e c} \\\\approx 2{,}426 \\\\times 10^{-12} \\\\, \\\\mathrm{m}",
  "physical_meaning": "Beweis für den Teilchencharakter des Lichts (Photonenstoß).",
  "validity_domain": "Relativistischer elastischer Stoß zwischen Photon und ruhendem Elektron.",
  "tags": ["Quantenmechanik", "Compton", "Photon"],
  "difficulty": 2
}
```
Viel Erfolg beim Lernen!"""

        # Extract and parse
        import re

        match = re.search(r"```json:card([\s\S]*?)```", mock_raw_ai_text)
        self.assertIsNotNone(match)
        card_json = json.loads(match.group(1).strip())

        # Test attributes
        self.assertEqual(card_json["deck_id"], "quantenmechanik")
        self.assertEqual(
            card_json["title"], "Compton-Streuung & Wellenlängenverschiebung"
        )
        self.assertIn(r"\Delta \lambda", card_json["back"])
        self.assertIsInstance(card_json["tags"], list)
        self.assertEqual(card_json["difficulty"], 2)

    def test_sanitize_card_latex(self):
        """Verify automatic healing and formatting of LaTeX in cards."""
        from core.gemini_service import sanitize_card_latex

        raw_card = {
            "title": "Masse-Energie",
            "front": "Wie lautet die Äquivalenz?",
            "back": "E_0 = m_0 c^2",
            "formula_breakdown": "- E_0: Ruheenergie [J]\n- m_0: Ruhemasse [kg]\n- c: Vakuumlichtgeschwindigkeit [m/s]\n- hbar: Wirkungsquantum",
            "physical_meaning": "Masse entspricht Energie. Merke: Energieerhaltung gilt.",
            "validity_domain": "Gilt für v << c und T -> 0.",
        }

        sanitized = sanitize_card_latex(raw_card)

        # 1. Back wrapped in $$...$$
        self.assertEqual(sanitized["back"], "$$E_0 = m_0 c^2$$")

        # 2. Formula breakdown variables and units wrapped in $...$
        self.assertIn(
            "$E_0$: Ruheenergie $[\\mathrm{J}]$", sanitized["formula_breakdown"]
        )
        self.assertIn(
            "$m_0$: Ruhemasse $[\\mathrm{kg}]$", sanitized["formula_breakdown"]
        )
        self.assertIn(r"$\hbar$: Wirkungsquantum", sanitized["formula_breakdown"])

        # 3. Validity domain relations
        self.assertIn(r"$v \ll c$", sanitized["validity_domain"])
        self.assertIn(r"$T \to 0$", sanitized["validity_domain"])

        # 4. Normal prose colons preserved without wrapping
        self.assertIn("Merke: Energieerhaltung gilt.", sanitized["physical_meaning"])
        self.assertNotIn("$Merke$", sanitized["physical_meaning"])


if __name__ == "__main__":
    unittest.main()
