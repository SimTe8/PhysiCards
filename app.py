"""
PhysiCards Flask Application & REST API
Provides endpoints for decks, cards, study queue, SM-2 reviews,
progress statistics, and export/import.
"""

import json
import uuid
from datetime import datetime, timezone

from flask import Flask, Response, jsonify, request, send_from_directory

from core.gemini_service import GeminiTutorService, sanitize_card_latex
from core.models import Card, Deck
from core.storage import Storage

app = Flask(__name__, static_folder="static", static_url_path="")
storage = Storage()
gemini_service = GeminiTutorService(storage)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ==========================================
# DECKS API
# ==========================================
@app.route("/api/decks", methods=["GET"])
def get_decks():
    decks = storage.get_decks()
    return jsonify({"success": True, "decks": decks})


@app.route("/api/decks/<deck_id>", methods=["GET"])
def get_deck(deck_id):
    deck = storage.get_deck(deck_id)
    if not deck:
        return jsonify({"success": False, "error": "Deck nicht gefunden"}), 404
    return jsonify({"success": True, "deck": deck})


@app.route("/api/decks", methods=["POST"])
def create_deck():
    data = request.json or {}
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"success": False, "error": "Deck-Name ist erforderlich"}), 400

    deck_id = data.get("id", "").strip() or f"deck_{uuid.uuid4().hex[:8]}"
    deck = Deck(
        id=deck_id,
        name=name,
        description=data.get("description", "").strip(),
        icon=data.get("icon", "atom"),
        color=data.get("color", "#3b82f6"),
    )
    result = storage.create_deck(deck)
    return jsonify({"success": True, "deck": result}), 201


@app.route("/api/decks/<deck_id>", methods=["PUT"])
def update_deck(deck_id):
    data = request.json or {}
    if "name" in data and not str(data["name"]).strip():
        return jsonify({"success": False, "error": "Name darf nicht leer sein"}), 400
    updated = storage.update_deck(deck_id, data)
    if not updated:
        return jsonify({"success": False, "error": "Deck nicht gefunden"}), 404
    return jsonify({"success": True, "deck": updated})


@app.route("/api/decks/<deck_id>", methods=["DELETE"])
def delete_deck(deck_id):
    storage.delete_deck(deck_id)
    return jsonify({"success": True, "message": "Deck gelöscht"})


@app.route("/api/decks/<deck_id>/reset", methods=["POST"])
def reset_deck(deck_id):
    storage.reset_deck_progress(deck_id)
    return jsonify(
        {"success": True, "message": "Lernfortschritt des Decks zurückgesetzt"}
    )


# ==========================================
# CARDS API
# ==========================================
@app.route("/api/cards", methods=["GET"])
def get_cards():
    deck_id = request.args.get("deck_id")
    search = request.args.get("search")
    tag = request.args.get("tag")
    cards = storage.get_cards(deck_id=deck_id, search=search, tag=tag)
    return jsonify({"success": True, "cards": cards, "total": len(cards)})


@app.route("/api/cards/<card_id>", methods=["GET"])
def get_card(card_id):
    card = storage.get_card(card_id)
    if not card:
        return jsonify({"success": False, "error": "Karte nicht gefunden"}), 404
    return jsonify({"success": True, "card": card})


@app.route("/api/cards", methods=["POST"])
def create_card():
    raw_data = request.json or {}
    data = sanitize_card_latex(raw_data)
    deck_id = data.get("deck_id", "").strip()
    title = data.get("title", "").strip()
    front = data.get("front", "").strip()
    back = data.get("back", "").strip()

    if not deck_id or not front or not back:
        return jsonify(
            {
                "success": False,
                "error": "Deck, Vorderseite und Rückseite sind erforderlich",
            }
        ), 400

    if not title:
        # Generate title from first line of front if empty
        title = front.split("\n")[0][:40].replace("*", "").replace("#", "").strip()

    card_id = data.get("id", "").strip() or f"card_{uuid.uuid4().hex[:10]}"
    card = Card(
        id=card_id,
        deck_id=deck_id,
        title=title,
        front=front,
        back=back,
        hint=data.get("hint", "").strip(),
        formula_breakdown=data.get("formula_breakdown", "").strip(),
        physical_meaning=data.get("physical_meaning", "").strip(),
        validity_domain=data.get("validity_domain", "").strip(),
        tags=data.get("tags", []),
        difficulty=int(data.get("difficulty", 3)),
    )
    result = storage.create_card(card)
    return jsonify({"success": True, "card": result}), 201


@app.route("/api/cards/<card_id>", methods=["PUT"])
def update_card(card_id):
    raw_data = request.json or {}
    data = sanitize_card_latex(raw_data)
    updated = storage.update_card(card_id, data)
    if not updated:
        return jsonify({"success": False, "error": "Karte nicht gefunden"}), 404
    return jsonify({"success": True, "card": updated})


@app.route("/api/cards/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    storage.delete_card(card_id)
    return jsonify({"success": True, "message": "Karte gelöscht"})


# ==========================================
# STUDY QUEUE & SM-2 REVIEWS
# ==========================================
@app.route("/api/study/queue", methods=["GET"])
def study_queue():
    deck_id = request.args.get("deck_id")
    mode = request.args.get("mode", "due")
    limit = int(request.args.get("limit", 50))
    queue = storage.get_study_queue(deck_id=deck_id, mode=mode, limit=limit)
    return jsonify({"success": True, "queue": queue, "total": len(queue)})


@app.route("/api/study/review", methods=["POST"])
def study_review():
    data = request.json or {}
    card_id = data.get("card_id")
    rating = data.get("rating")
    response_time_ms = int(data.get("response_time_ms", 0))

    if not card_id or rating not in [1, 2, 3, 4]:
        return jsonify(
            {"success": False, "error": "Ungültiges Rating (1-4 erforderlich)"}
        ), 400

    try:
        result = storage.record_review(card_id, rating, response_time_ms)
        return jsonify({"success": True, "review": result})
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 404


# ==========================================
# STATS & ANALYTICS
# ==========================================
@app.route("/api/stats", methods=["GET"])
def get_stats():
    stats = storage.get_stats()
    return jsonify({"success": True, "stats": stats})


# ==========================================
# EXPORT & IMPORT
# ==========================================
@app.route("/api/export", methods=["GET"])
def export_data():
    data = storage.export_all()
    filename = (
        f"physicards_backup_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    )
    return Response(
        json.dumps(data, indent=2, ensure_ascii=False),
        mimetype="application/json",
        headers={"Content-Disposition": f"attachment;filename={filename}"},
    )


@app.route("/api/import", methods=["POST"])
def import_data():
    data = request.json
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "error": "Ungültiges JSON-Format"}), 400

    decks_cnt, cards_cnt = storage.import_all(data)
    return jsonify(
        {
            "success": True,
            "message": f"{decks_cnt} Decks und {cards_cnt} Karten erfolgreich importiert.",
        }
    )


@app.route("/api/export/anki", methods=["GET"])
def export_anki():
    deck_id = request.args.get("deck_id")
    cards = storage.get_cards(deck_id=deck_id)
    lines = ["#separator:tab", "#html:true", "#tags column:3"]
    for c in cards:
        # Clean front and back for TSV
        f = c["front"].replace("\t", " ").replace("\n", "<br>")
        b = c["back"].replace("\t", " ").replace("\n", "<br>")
        if c.get("formula_breakdown"):
            b += (
                "<br><hr><small><b>Variablen & Einheiten:</b><br>"
                + c["formula_breakdown"].replace("\t", " ").replace("\n", "<br>")
                + "</small>"
            )
        tags = " ".join(c.get("tags", []))
        lines.append(f"{f}\t{b}\t{tags}")

    tsv_content = "\n".join(lines)
    filename = f"physicards_anki_{deck_id or 'all'}.tsv"
    return Response(
        tsv_content,
        mimetype="text/tab-separated-values; charset=utf-8",
        headers={"Content-Disposition": f"attachment;filename={filename}"},
    )


# ==========================================
# GEMINI AI TUTOR & GENERATOR API
# ==========================================
@app.route("/api/ai/settings", methods=["GET"])
def get_ai_settings():
    key = gemini_service.get_api_key()
    masked = f"{key[:6]}...{key[-4:]}" if len(key) >= 10 else ("***" if key else "")
    return jsonify(
        {
            "success": True,
            "has_key": bool(key),
            "masked_key": masked,
            "api_key": key,
            "model": gemini_service.get_model(),
            "style": gemini_service.get_tutor_style(),
            "available_models": gemini_service.get_available_models(),
        }
    )


@app.route("/api/ai/settings", methods=["POST"])
def update_ai_settings():
    data = request.json or {}
    if "api_key" in data:
        new_key = str(data["api_key"]).strip()
        if new_key:
            storage.set_setting("gemini_api_key", new_key)
        else:
            storage.delete_setting("gemini_api_key")
    if "model" in data:
        storage.set_setting("gemini_model", data["model"].strip())
    if "style" in data:
        storage.set_setting("gemini_style", data["style"].strip())
    return jsonify({"success": True, "message": "KI-Einstellungen gespeichert."})


@app.route("/api/ai/test", methods=["POST"])
def test_ai_connection():
    data = request.json or {}
    key = data.get("api_key") or gemini_service.get_api_key()
    model = data.get("model") or gemini_service.get_model()
    result = gemini_service.test_connection(api_key=key, model=model)
    return jsonify(result)


@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    data = request.json or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify(
            {"success": False, "error": "Nachricht darf nicht leer sein."}
        ), 400

    card_id = data.get("card_id")
    card = None
    if card_id:
        card_dict = storage.get_card(card_id)
        if card_dict:
            card = Card(
                id=card_dict["id"],
                deck_id=card_dict["deck_id"],
                title=card_dict["title"],
                front=card_dict["front"],
                back=card_dict["back"],
                hint=card_dict.get("hint") or "",
                formula_breakdown=card_dict.get("formula_breakdown") or "",
                physical_meaning=card_dict.get("physical_meaning") or "",
                validity_domain=card_dict.get("validity_domain") or "",
                tags=card_dict.get("tags") or [],
                difficulty=card_dict.get("difficulty") or 3,
                created_at=card_dict.get("created_at") or "",
                updated_at=card_dict.get("updated_at") or "",
            )

    history = data.get("history", [])
    style = data.get("style") or gemini_service.get_tutor_style()

    def generate_stream():
        yield from gemini_service.stream_chat(
            card=card,
            user_message=user_message,
            history=history,
            style=style,
        )

    return Response(
        generate_stream(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.route("/api/ai/generate-card", methods=["POST"])
def ai_generate_card():
    data = request.json or {}
    topic = data.get("topic", "").strip()
    deck_id = data.get("deck_id")
    if not topic:
        return jsonify({"success": False, "error": "Thema ist erforderlich."}), 400

    result = gemini_service.generate_card_from_topic(topic=topic, deck_id=deck_id)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5055, debug=True)
