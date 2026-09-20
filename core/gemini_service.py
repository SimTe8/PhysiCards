"""
Gemini AI Tutor and Card Generator Service.
Connects PhysiCards with Google AI Studio API for interactive Socratic physics tutoring,
real-time SSE streaming, and automated standardized flashcard generation.
100% zero external dependencies (uses standard library urllib.request).
"""

import json
import os
import re
import ssl
import urllib.error
import urllib.request
from collections.abc import Generator
from typing import Any

from core.models import Card

DEFAULT_MODEL = "gemini-3.6-flash"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"

AVAILABLE_MODELS = [
    {
        "id": "gemini-3.6-flash",
        "name": "Gemini 3.6 Flash (Empfohlen - Schnell & Stark)",
        "badge": "Standard",
        "description": "Aktuelles Google AI Studio Standardmodell. Schnell, präzise und ideal für den täglichen Lerndialog.",
    },
    {
        "id": "gemini-3.1-pro-preview",
        "name": "Gemini 3.1 Pro Preview (Google AI Pro - Höchste Intelligenz)",
        "badge": "Pro",
        "description": "Frontier-Modell der 3. Generation für komplexe mathematische Herleitungen, Symmetrien und physikalische Beweise.",
    },
    {
        "id": "gemini-3.8-flash",
        "name": "Gemini 3.8 Flash (Neueste Generation)",
        "badge": "Neu",
        "description": "Neuestes Flash-Modell mit erweiterten Reasoning- und Formulierungskompetenzen.",
    },
    {
        "id": "gemini-3.7-flash",
        "name": "Gemini 3.7 Flash",
        "badge": "Stabil",
        "description": "Schnelles, zuverlässiges Vorgängermodell für flüssige Dialoge.",
    },
]

DEPRECATED_MODELS = {
    "gemini-2.5-flash": "gemini-3.6-flash",
    "gemini-2.0-flash": "gemini-3.6-flash",
    "gemini-2.0-flash-001": "gemini-3.6-flash",
    "gemini-2.0-flash-lite": "gemini-3.6-flash",
    "gemini-1.5-flash": "gemini-3.6-flash",
    "gemini-1.5-pro": "gemini-3.1-pro-preview",
}

GREEK_LETTERS = [
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "zeta",
    "eta",
    "theta",
    "iota",
    "kappa",
    "lambda",
    "mu",
    "nu",
    "xi",
    "pi",
    "rho",
    "sigma",
    "tau",
    "upsilon",
    "phi",
    "chi",
    "psi",
    "omega",
    "Delta",
    "Gamma",
    "Theta",
    "Lambda",
    "Xi",
    "Pi",
    "Sigma",
    "Phi",
    "Psi",
    "Omega",
    "hbar",
]


def is_math_variable(s: str) -> bool:
    """Checks if a string looks like a mathematical variable or symbol rather than prose."""
    s = s.strip()
    if not s or len(s) > 20:
        return False
    words = s.split()
    if len(words) > 2:
        return False
    if any(len(w) > 8 for w in words):
        return False
    if any(c in "äöüÄÖÜß" for c in s):
        return False
    return True


def sanitize_math_text(text: str, is_breakdown: bool = False) -> str:
    """
    Ensures mathematical symbols, variables, formulas, and units are properly wrapped in LaTeX $ ... $.
    Safe against double-wrapping and regular text.
    """
    if not text:
        return text

    lines = text.split("\n")
    processed_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            processed_lines.append(line)
            continue

        # Bullet point line detection: starts with - or *
        bullet_match = re.match(r"^(\s*[\-\*]\s*)(.*)$", line)
        if bullet_match:
            bullet_prefix = bullet_match.group(1)
            content = bullet_match.group(2)
        else:
            bullet_prefix = ""
            content = line

        # Check for symbol definition before a colon ONLY for bullet breakdown lines
        colon_idx = content.find(":")
        if (
            is_breakdown
            and bullet_prefix
            and colon_idx != -1
            and not content.startswith("http")
        ):
            sym_part = content[:colon_idx].strip()
            rest_part = content[colon_idx:]  # includes ':'

            # If sym_part does not contain $, wrap it if it looks like a variable/math
            if "$" not in sym_part and is_math_variable(sym_part):
                for greek in GREEK_LETTERS:
                    sym_part = re.sub(rf"(?<!\\)\b{greek}\b", rf"\\{greek}", sym_part)
                sym_part = f"${sym_part}$"

            content = f"{sym_part}{rest_part}"

        # Convert brackets with units like [J] or [m/s] into $[\mathrm{...}]$ if not inside $
        def wrap_unit(m: re.Match[str]) -> str:
            u = m.group(1).strip()
            if "$" in u or not u or any(c in "äöüÄÖÜ" for c in u):
                return m.group(0)
            return f"$[\\mathrm{{{u}}}]$"

        content = re.sub(r"\[([^\]\$]+)\]", wrap_unit, content)

        # Handle relational physics expressions outside $ ... $
        parts = re.split(r"(\$\$[\s\S]*?\$\$|\$[^\$]+?\$)", content)
        for i in range(0, len(parts), 2):
            plain = parts[i]
            plain = re.sub(
                r"\b([a-zA-Z_0-9]+)\s*<<\s*([a-zA-Z_0-9]+)\b", r"$\1 \\ll \2$", plain
            )
            plain = re.sub(
                r"\b([a-zA-Z_0-9]+)\s*>>\s*([a-zA-Z_0-9]+)\b", r"$\1 \\gg \2$", plain
            )
            plain = re.sub(
                r"\b([a-zA-Z_0-9]+)\s*<=\s*([a-zA-Z_0-9]+)\b", r"$\1 \\le \2$", plain
            )
            plain = re.sub(
                r"\b([a-zA-Z_0-9]+)\s*>=\s*([a-zA-Z_0-9]+)\b", r"$\1 \\ge \2$", plain
            )
            plain = re.sub(r"\b([a-zA-Z_0-9]+)\s*->\s*0\b", r"$\1 \\to 0$", plain)
            parts[i] = plain

        processed_lines.append(f"{bullet_prefix}{''.join(parts)}")

    return "\n".join(processed_lines)


def sanitize_card_latex(card_data: dict[str, Any]) -> dict[str, Any]:
    """
    Sanitizes all fields of a card dictionary to ensure full LaTeX formatting compliance.
    """
    c = dict(card_data)

    # 1. Back formula: if no $ and contains formula symbols, wrap in $$...$$
    back = str(c.get("back", "")).strip()
    if back and "$" not in back:
        if any(sym in back for sym in ["=", "\\", "^", "_", "+", "-", "/", "*"]):
            c["back"] = f"$${back}$$"

    # 2. Formula breakdown
    if c.get("formula_breakdown"):
        c["formula_breakdown"] = sanitize_math_text(
            str(c["formula_breakdown"]), is_breakdown=True
        )

    # 3. Physical meaning
    if c.get("physical_meaning"):
        c["physical_meaning"] = sanitize_math_text(
            str(c["physical_meaning"]), is_breakdown=False
        )

    # 4. Validity domain
    if c.get("validity_domain"):
        c["validity_domain"] = sanitize_math_text(
            str(c["validity_domain"]), is_breakdown=False
        )

    # 5. Front & Hint
    if c.get("front"):
        c["front"] = sanitize_math_text(str(c["front"]), is_breakdown=False)
    if c.get("hint"):
        c["hint"] = sanitize_math_text(str(c["hint"]), is_breakdown=False)

    return c


def get_system_prompt(card: Card | None = None, style: str = "socratic") -> str:
    """Constructs a pedagogical system prompt with card context and tutoring style."""
    base_instructions = """Du bist der KI-Physik-Tutor für 'PhysiCards', ein spezialisiertes Lernsystem für Physik und mathematische Methoden.
Deine Rolle ist es, den Lernenden dabei zu unterstützen, ein tiefes physikalisches Verständnis und echte Intuition zu entwickeln, anstatt nur Formeln mechanisch auswendig zu lernen.

Regeln für deine Antworten:
1. MATHEMATISCHE FORMELN & PHYSIKALISCHE GRÖSSEN (STRIKTE LATEX-PFLICHT):
   - Schreibe AUSNAHMSLOS alle mathematischen Symbole, Variablen, Gleichungen und physikalischen Einheiten in sauberer LaTeX-Syntax mit Dollarzeichen!
   - Inline-Formeln in $...$ (z.B. $E = mc^2$, $\\nabla \\times \\vec{E}$, $\\hbar$, $v \\ll c$).
   - Auch einzelne Variablen wie $v$, $c$, $m$, $T$, $E$, $\\lambda$, $p$, $\\Delta x$ NIEMALS ohne Dollarzeichen schreiben!
   - Abgesetzte Formeln in $$...$$ auf eigener Zeile.
   - Verwende \\mathrm{...} für SI-Einheiten in eckigen Klammern: z.B. $[\\mathrm{J}]$, $[\\mathrm{kg\\cdot m^2/s^2}]$, $[\\mathrm{m/s}]$.

2. DIDAKTISCHER STIL:
"""
    if style == "socratic":
        base_instructions += """   - Sei sokratisch: Stelle gezielte Gegenfragen, bringe den Lernenden dazu, Grenzfälle zu durchdenken (z.B. 'Was passiert, wenn $v \\to c$ geht oder $T \\to 0$?').
   - Bestätige richtige Ansätze und korrigiere Fehlannahmen wohlwollend und präzise.\n"""
    elif style == "intuitive":
        base_instructions += """   - Fokussiere auf Alltags-Analogien, Gedankenexperimente und geometrische Anschauung.
   - Erkläre, WARUM eine Naturkonstante oder ein Exponent genau so dasteht, wie er dasteht.\n"""
    elif style == "rigorous":
        base_instructions += """   - Biete präzise mathematische Herleitungen, Symmetriebetrachtungen und saubere vektoranalytische Zwischenschritte.\n"""
    else:
        base_instructions += """   - Erkläre klar, didaktisch ausgewogen und hebe physikalische Intuition hervor.\n"""

    base_instructions += """
3. AUTOMATISIERTE KARTEIKARTEN-ERSTELLUNG (STRIKTES LATEX IN JEDEM FELD):
   - Wenn der Nutzer dich bittet, eine neue Karteikarte zu erstellen (oder den Befehl 'Erstelle eine Karteikarte' / 'Als Karte speichern' gibt), liefere neben deiner kurzen Erklärung das standardisierte Karten-JSON-Objekt in einem Markdown-Codeblock mit dem Präfix ```json:card:
   ```json:card
   {
     "deck_id": "mechanik | elektrodynamik | quantenmechanik | thermodynamik | relativitaet | mathe_physik | konstanten",
     "title": "Prägnanter Titel der Karte",
     "front": "Klare Fragestellung mit LaTeX, z.B. 'Wie lautet die Formel für $E$?'",
     "back": "Exakte Antwort / Formel mit LaTeX, z.B. '$$E = mc^2$$'",
     "hint": "Hilfreicher Denkanstoß mit $...$",
     "formula_breakdown": "- $E$: Gesamtenergie $[\\\\mathrm{J}]$\\n- $m$: Masse $[\\\\mathrm{kg}]$\\n- $c$: Lichtgeschwindigkeit $[\\\\mathrm{m/s}]$",
     "physical_meaning": "Fundamentale Intuition: Masse entspricht konzentrierter Energie ($E = mc^2$).",
     "validity_domain": "Gültigkeitsbereich, z.B. 'Exakt im Ruhesystem ($p = 0$) bzw. $v \\\\ll c$'.",
     "tags": ["Thema1", "Thema2"],
     "difficulty": 2
   }
   ```
   WICHTIG: In 'formula_breakdown', 'physical_meaning' und 'validity_domain' dürfen NIEMALS Variablen oder Formeln ohne $...$ stehen!
"""

    if card:
        base_instructions += f"""
AKTUELLE KARTEIKARTE IM FOKUS DES NUTZERS:
- Titel: {card.title}
- Deck: {card.deck_id}
- Vorderseite (Frage): {card.front}
- Rückseite (Formel/Antwort): {card.back}
- Formelaufschlüsselung / Einheiten: {card.formula_breakdown or "Keine"}
- Physikalische Bedeutung: {card.physical_meaning or "Keine"}
- Gültigkeitsbereich: {card.validity_domain or "Allgemein"}
- Tags: {", ".join(card.tags)}
Beziehe dich direkt auf diese Inhalte, wenn der Nutzer Fragen dazu stellt.
"""
    return base_instructions


class GeminiTutorService:
    def __init__(self, storage: Any):
        self.storage = storage

    def get_api_key(self) -> str:
        """Retrieves the API key from database settings or environment variable."""
        key = self.storage.get_setting("gemini_api_key")
        if key and key.strip():
            return key.strip()
        return os.environ.get("GEMINI_API_KEY", "").strip()

    def get_model(self) -> str:
        """Retrieves configured model or fallback default. Automatically migrates deprecated models."""
        raw_model = (self.storage.get_setting("gemini_model") or DEFAULT_MODEL).strip()
        if raw_model in DEPRECATED_MODELS:
            migrated_model = DEPRECATED_MODELS[raw_model]
            self.storage.set_setting("gemini_model", migrated_model)
            return migrated_model
        return raw_model

    def get_available_models(self) -> list[dict[str, Any]]:
        """Returns list of curated and supported models."""
        return AVAILABLE_MODELS

    def get_tutor_style(self) -> str:
        """Retrieves configured tutor style."""
        return self.storage.get_setting("gemini_style") or "socratic"

    def test_connection(
        self, api_key: str | None = None, model: str | None = None
    ) -> dict[str, Any]:
        """Validates the API key and model connectivity."""
        key = api_key or self.get_api_key()
        if not key:
            return {
                "success": False,
                "error": "Kein Google AI Studio API-Key hinterlegt. Bitte trage deinen Key in den Einstellungen ein.",
            }

        target_model = model or self.get_model()
        url = f"{GEMINI_API_BASE}/models/{target_model}:generateContent?key={key}"

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": "Antworte mit exakt einem Wort: 'Bereit'."}],
                }
            ],
            "generationConfig": {"maxOutputTokens": 10, "temperature": 0.0},
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    return {
                        "success": True,
                        "model": target_model,
                        "message": "Verbindung zu Google AI Studio erfolgreich hergestellt!",
                    }
                return {
                    "success": False,
                    "error": "Unerwartete Antwort von Gemini API.",
                }
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_body)
                msg = err_json.get("error", {}).get("message", str(e))
            except Exception:
                msg = f"HTTP {e.code}: {e.reason}"
            return {"success": False, "error": f"API-Fehler: {msg}"}
        except urllib.error.URLError as e:
            return {
                "success": False,
                "error": f"Netzwerkfehler (Offline?): {e.reason}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def stream_chat(
        self,
        card: Card | None,
        user_message: str,
        history: list[dict[str, str]] | None = None,
        style: str | None = None,
    ) -> Generator[str, None, None]:
        """
        Streams chat responses from Gemini using Server-Sent Events (SSE).
        Yields text deltas formatted for SSE.
        """
        api_key = self.get_api_key()
        if not api_key:
            yield f"data: {json.dumps({'error': 'Kein API-Key hinterlegt. Bitte öffne die Einstellungen ⚙️ und gib deinen Google AI Studio API-Key ein, um den KI-Tutor zu aktivieren.'})}\n\n"
            yield "data: [DONE]\n\n"
            return

        model = self.get_model()
        tutor_style = style or self.get_tutor_style()
        system_prompt = get_system_prompt(card, tutor_style)

        # Build contents array
        contents = []
        if history:
            for turn in history:
                role = "user" if turn.get("role") == "user" else "model"
                text = turn.get("content", "").strip()
                if text:
                    contents.append({"role": role, "parts": [{"text": text}]})

        contents.append({"role": "user", "parts": [{"text": user_message.strip()}]})

        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 8192,
            },
        }

        url = f"{GEMINI_API_BASE}/models/{model}:streamGenerateContent?alt=sse&key={api_key}"

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, context=ctx, timeout=90) as resp:
                for raw_line in resp:
                    line = raw_line.decode("utf-8")
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if not data_str:
                            continue
                        try:
                            chunk = json.loads(data_str)
                            candidates = chunk.get("candidates", [])
                            if candidates:
                                candidate = candidates[0]
                                parts = candidate.get("content", {}).get("parts", [])
                                for part in parts:
                                    # Skip raw thought parts from internal chain-of-thought
                                    if part.get("thought"):
                                        continue
                                    text = part.get("text", "")
                                    if text:
                                        yield f"data: {json.dumps({'text': text})}\n\n"

                                finish_reason = candidate.get("finishReason")
                                if finish_reason == "MAX_TOKENS":
                                    yield f"data: {json.dumps({'text': '\n\n*(Antwort wurde aufgrund des Token-Limits gekürzt. Du kannst mit „Fahre fort“ die Antwort weiterführen.)*'})}\n\n"
                        except json.JSONDecodeError:
                            continue

            yield "data: [DONE]\n\n"

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_body)
                err_msg = err_json.get("error", {}).get("message", str(e))
            except Exception:
                err_msg = f"HTTP {e.code}: {e.reason}"
            yield f"data: {json.dumps({'error': f'Gemini API Fehler: {err_msg}'})}\n\n"
            yield "data: [DONE]\n\n"
        except urllib.error.URLError as e:
            yield f"data: {json.dumps({'error': f'Verbindungsfehler (Offline?): {e.reason}'})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': f'Unerwarteter Fehler: {e!s}'})}\n\n"
            yield "data: [DONE]\n\n"

    def generate_card_from_topic(
        self, topic: str, deck_id: str | None = None
    ) -> dict[str, Any]:
        """
        Generates a standardized Card dictionary for a given physics topic.
        """
        api_key = self.get_api_key()
        if not api_key:
            return {
                "success": False,
                "error": "Kein Google AI Studio API-Key hinterlegt.",
            }

        model = self.get_model()
        url = f"{GEMINI_API_BASE}/models/{model}:generateContent?key={api_key}"

        prompt = f"""Erstelle eine didaktisch hochwertige Physik-Karteikarte zum Thema: '{topic}'.
Ziel-Deck (falls passend): {deck_id or "wähle das am besten passende Deck: mechanik, elektrodynamik, quantenmechanik, thermodynamik, relativitaet, mathe_physik, konstanten"}.

WICHTIGSTE VORSCHRIFT FÜR LATEX:
Alle mathematischen Symbole, Variablen, Einheiten und Gleichungen in ALLEN Feldern MÜSSEN ausnahmslos in LaTeX-Dollarzeichen gefasst sein ($...$ oder $$...$$)!
Schreibe niemals Variablen oder Einheiten ohne Dollarzeichen!
Beispiel für formula_breakdown:
- $E$: Gesamtenergie $[\\mathrm{J}]$
- $m$: Masse $[\\mathrm{kg}]$
- $c$: Vakuumlichtgeschwindigkeit $[\\mathrm{m / s}]$

Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt im folgenden Format:
{{
  "deck_id": "{deck_id or "mechanik"}",
  "title": "Prägnanter Titel",
  "front": "Frage- bzw. Problemstellung mit sauberem LaTeX ($...$)",
  "back": "Exakte Lösung und Formel mit sauberem LaTeX ($$...$$)",
  "hint": "Hilfreicher Tipp für den Lernenden mit $...$",
  "formula_breakdown": "- $E$: Energie $[\\mathrm{J}]$\\n- $c$: Lichtgeschwindigkeit $[\\mathrm{m / s}]$",
  "physical_meaning": "Fundamentale physikalische Intuition mit Variablen in $...$",
  "validity_domain": "Gültigkeitsbereich und Grenzfälle mit $...$ (z.B. $v \\ll c$, $T \\to 0$)",
  "tags": ["Physik", "{topic}"],
  "difficulty": 2
}}"""

        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 4096,
                "responseMimeType": "application/json",
            },
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, context=ctx, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if not candidates:
                    return {
                        "success": False,
                        "error": "Keine Antwort von Gemini erhalten.",
                    }

                content_text = candidates[0]["content"]["parts"][0]["text"]
                # Clean up JSON if wrapped in markdown
                match = re.search(r"\{[\s\S]*\}", content_text)
                if match:
                    card_dict = json.loads(match.group(0))
                    # Sanitize and ensure all fields exist
                    card_data = {
                        "deck_id": card_dict.get("deck_id") or deck_id or "mechanik",
                        "title": card_dict.get("title") or f"Physik: {topic}",
                        "front": card_dict.get("front") or "",
                        "back": card_dict.get("back") or "",
                        "hint": card_dict.get("hint") or "",
                        "formula_breakdown": card_dict.get("formula_breakdown") or "",
                        "physical_meaning": card_dict.get("physical_meaning") or "",
                        "validity_domain": card_dict.get("validity_domain") or "",
                        "tags": card_dict.get("tags") or [topic],
                        "difficulty": int(card_dict.get("difficulty") or 2),
                    }
                    card_data = sanitize_card_latex(card_data)
                    return {"success": True, "card": card_data}
                return {
                    "success": False,
                    "error": "Antwort konnte nicht als Karte parst werden.",
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
