"""
SQLite Database storage layer for PhysiCards.
Handles schema initialization, seeding default physics decks, CRUD,
study queue management, and statistics tracking.
"""

import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

from core.default_decks import get_default_cards, get_default_decks
from core.models import Card, Deck, ReviewState
from core.sm2 import calculate_sm2, predict_intervals

DB_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)
DB_PATH = os.path.join(DB_DIR, "cards.db")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class Storage:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS decks (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    icon TEXT DEFAULT 'atom',
                    color TEXT DEFAULT '#3b82f6',
                    created_at TEXT NOT NULL
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS cards (
                    id TEXT PRIMARY KEY,
                    deck_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    front TEXT NOT NULL,
                    back TEXT NOT NULL,
                    hint TEXT,
                    formula_breakdown TEXT,
                    physical_meaning TEXT,
                    validity_domain TEXT,
                    tags TEXT,
                    difficulty INTEGER DEFAULT 3,
                    has_cloze INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS review_state (
                    card_id TEXT PRIMARY KEY,
                    repetitions INTEGER DEFAULT 0,
                    interval_days REAL DEFAULT 0.0,
                    ease_factor REAL DEFAULT 2.5,
                    next_due TEXT NOT NULL,
                    last_reviewed TEXT,
                    total_reviews INTEGER DEFAULT 0,
                    lapses INTEGER DEFAULT 0,
                    last_quality INTEGER,
                    FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS study_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_id TEXT NOT NULL,
                    deck_id TEXT NOT NULL,
                    quality INTEGER NOT NULL,
                    interval_days REAL NOT NULL,
                    ease_factor REAL NOT NULL,
                    response_time_ms INTEGER DEFAULT 0,
                    timestamp TEXT NOT NULL
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

        # Sync default physics decks and cards (adds new ones without overwriting existing)
        self.sync_default_decks_and_cards()

    def seed_defaults_if_empty(self):
        """Backward compatible wrapper around sync_default_decks_and_cards."""
        self.sync_default_decks_and_cards()

    def sync_default_decks_and_cards(self):
        """
        Inserts any missing default decks and cards into SQLite.
        Uses INSERT OR IGNORE so existing user cards, custom decks, and review states
        are preserved completely.
        """
        decks = get_default_decks()
        cards = get_default_cards()
        now = utc_now_iso()

        with self.get_connection() as conn:
            c = conn.cursor()
            for d in decks:
                c.execute(
                    """
                    INSERT OR IGNORE INTO decks (id, name, description, icon, color, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (d.id, d.name, d.description, d.icon, d.color, d.created_at),
                )

            for card in cards:
                tags_json = json.dumps(card.tags, ensure_ascii=False)
                has_cloze = 1 if ("{{" in card.front or "{{" in card.back) else 0
                c.execute(
                    """
                    INSERT OR IGNORE INTO cards (
                        id, deck_id, title, front, back, hint,
                        formula_breakdown, physical_meaning, validity_domain,
                        tags, difficulty, has_cloze, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        card.id,
                        card.deck_id,
                        card.title,
                        card.front,
                        card.back,
                        card.hint,
                        card.formula_breakdown,
                        card.physical_meaning,
                        card.validity_domain,
                        tags_json,
                        card.difficulty,
                        has_cloze,
                        card.created_at,
                        card.updated_at,
                    ),
                )
                # Initial review state if not existing
                c.execute(
                    """
                    INSERT OR IGNORE INTO review_state (card_id, repetitions, interval_days, ease_factor, next_due, total_reviews, lapses)
                    VALUES (?, 0, 0.0, 2.5, ?, 0, 0)
                """,
                    (card.id, now),
                )

            conn.commit()

    # ==========================================
    # DECKS CRUD & STATS
    # ==========================================
    def get_decks(self) -> list[dict[str, Any]]:
        now = utc_now_iso()
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                SELECT d.*,
                    COUNT(c.id) as total_cards,
                    SUM(CASE WHEN r.next_due <= ? OR r.repetitions = 0 THEN 1 ELSE 0 END) as due_cards,
                    SUM(CASE WHEN r.repetitions >= 3 THEN 1 ELSE 0 END) as mastered_cards,
                    SUM(CASE WHEN r.repetitions = 0 THEN 1 ELSE 0 END) as new_cards
                FROM decks d
                LEFT JOIN cards c ON d.id = c.deck_id
                LEFT JOIN review_state r ON c.id = r.card_id
                GROUP BY d.id
                ORDER BY d.created_at ASC
            """,
                (now,),
            )
            rows = c.fetchall()
            return [dict(r) for r in rows]

    def get_deck(self, deck_id: str) -> dict[str, Any] | None:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM decks WHERE id = ?", (deck_id,))
            row = c.fetchone()
            return dict(row) if row else None

    def create_deck(self, deck: Deck) -> dict[str, Any]:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO decks (id, name, description, icon, color, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    deck.id,
                    deck.name,
                    deck.description,
                    deck.icon,
                    deck.color,
                    deck.created_at,
                ),
            )
            conn.commit()
        return deck.to_dict()

    def update_deck(self, deck_id: str, data: dict[str, Any]) -> dict[str, Any] | None:
        with self.get_connection() as conn:
            c = conn.cursor()
            fields = []
            values = []
            for k in ["name", "description", "icon", "color"]:
                if k in data:
                    fields.append(f"{k} = ?")
                    values.append(data[k])
            if not fields:
                return self.get_deck(deck_id)
            values.append(deck_id)
            c.execute(f"UPDATE decks SET {', '.join(fields)} WHERE id = ?", values)
            conn.commit()
        return self.get_deck(deck_id)

    def delete_deck(self, deck_id: str) -> bool:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
            c.execute("DELETE FROM cards WHERE deck_id = ?", (deck_id,))
            conn.commit()
        return True

    # ==========================================
    # CARDS CRUD
    # ==========================================
    def get_cards(
        self,
        deck_id: str | None = None,
        search: str | None = None,
        tag: str | None = None,
    ) -> list[dict[str, Any]]:
        with self.get_connection() as conn:
            c = conn.cursor()
            query = """
                SELECT c.*, d.name as deck_name, r.repetitions, r.interval_days, r.ease_factor, r.next_due, r.last_reviewed, r.total_reviews
                FROM cards c
                JOIN decks d ON c.deck_id = d.id
                LEFT JOIN review_state r ON c.id = r.card_id
                WHERE 1=1
            """
            params = []
            if deck_id:
                query += " AND c.deck_id = ?"
                params.append(deck_id)
            if search:
                query += " AND (c.title LIKE ? OR c.front LIKE ? OR c.back LIKE ? OR c.formula_breakdown LIKE ?)"
                term = f"%{search}%"
                params.extend([term, term, term, term])
            if tag:
                query += " AND c.tags LIKE ?"
                params.append(f"%{tag}%")

            query += " ORDER BY c.created_at DESC"
            c.execute(query, params)
            rows = c.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                item["tags"] = json.loads(item["tags"]) if item.get("tags") else []
                item["has_cloze"] = bool(item.get("has_cloze"))
                results.append(item)
            return results

    def get_card(self, card_id: str) -> dict[str, Any] | None:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                SELECT c.*, d.name as deck_name, r.repetitions, r.interval_days, r.ease_factor, r.next_due, r.last_reviewed, r.total_reviews, r.lapses
                FROM cards c
                JOIN decks d ON c.deck_id = d.id
                LEFT JOIN review_state r ON c.id = r.card_id
                WHERE c.id = ?
            """,
                (card_id,),
            )
            row = c.fetchone()
            if not row:
                return None
            item = dict(row)
            item["tags"] = json.loads(item["tags"]) if item.get("tags") else []
            item["has_cloze"] = bool(item.get("has_cloze"))
            return item

    def create_card(self, card: Card) -> dict[str, Any]:
        with self.get_connection() as conn:
            c = conn.cursor()
            tags_json = json.dumps(card.tags, ensure_ascii=False)
            has_cloze = 1 if ("{{" in card.front or "{{" in card.back) else 0
            c.execute(
                """
                INSERT INTO cards (
                    id, deck_id, title, front, back, hint,
                    formula_breakdown, physical_meaning, validity_domain,
                    tags, difficulty, has_cloze, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    card.id,
                    card.deck_id,
                    card.title,
                    card.front,
                    card.back,
                    card.hint,
                    card.formula_breakdown,
                    card.physical_meaning,
                    card.validity_domain,
                    tags_json,
                    card.difficulty,
                    has_cloze,
                    card.created_at,
                    card.updated_at,
                ),
            )
            now = utc_now_iso()
            c.execute(
                """
                INSERT INTO review_state (card_id, repetitions, interval_days, ease_factor, next_due, total_reviews, lapses)
                VALUES (?, 0, 0.0, 2.5, ?, 0, 0)
            """,
                (card.id, now),
            )
            conn.commit()
        return self.get_card(card.id)

    def update_card(self, card_id: str, data: dict[str, Any]) -> dict[str, Any] | None:
        with self.get_connection() as conn:
            c = conn.cursor()
            fields = []
            values = []
            updatable = [
                "deck_id",
                "title",
                "front",
                "back",
                "hint",
                "formula_breakdown",
                "physical_meaning",
                "validity_domain",
                "difficulty",
            ]
            for k in updatable:
                if k in data:
                    fields.append(f"{k} = ?")
                    values.append(data[k])
            if "tags" in data:
                fields.append("tags = ?")
                values.append(json.dumps(data["tags"], ensure_ascii=False))

            front_text = data.get("front", "")
            back_text = data.get("back", "")
            if "front" in data or "back" in data:
                has_cloze = 1 if ("{{" in front_text or "{{" in back_text) else 0
                fields.append("has_cloze = ?")
                values.append(has_cloze)

            fields.append("updated_at = ?")
            values.append(utc_now_iso())

            values.append(card_id)
            c.execute(f"UPDATE cards SET {', '.join(fields)} WHERE id = ?", values)
            conn.commit()
        return self.get_card(card_id)

    def delete_card(self, card_id: str) -> bool:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM cards WHERE id = ?", (card_id,))
            c.execute("DELETE FROM review_state WHERE card_id = ?", (card_id,))
            conn.commit()
        return True

    # ==========================================
    # STUDY QUEUE & SM-2 REVIEWS
    # ==========================================
    def get_study_queue(
        self, deck_id: str | None = None, mode: str = "due", limit: int = 50
    ) -> list[dict[str, Any]]:
        now = utc_now_iso()
        with self.get_connection() as conn:
            c = conn.cursor()
            query = """
                SELECT c.*, d.name as deck_name, d.color as deck_color,
                       r.repetitions, r.interval_days, r.ease_factor, r.next_due, r.last_reviewed, r.total_reviews, r.lapses
                FROM cards c
                JOIN decks d ON c.deck_id = d.id
                JOIN review_state r ON c.id = r.card_id
                WHERE 1=1
            """
            params = []
            if deck_id:
                query += " AND c.deck_id = ?"
                params.append(deck_id)

            if mode == "due":
                query += " AND (r.next_due <= ? OR r.repetitions = 0)"
                params.append(now)
                query += " ORDER BY r.repetitions ASC, r.next_due ASC"
            elif mode == "new":
                query += " AND r.repetitions = 0"
                query += " ORDER BY c.created_at ASC"
            elif mode == "difficult":
                query += " AND (r.lapses > 0 OR c.difficulty >= 4)"
                query += " ORDER BY r.lapses DESC, c.difficulty DESC"
            else:  # "all"
                query += " ORDER BY RANDOM()"

            query += f" LIMIT {limit}"
            c.execute(query, params)
            rows = c.fetchall()

            queue = []
            for row in rows:
                item = dict(row)
                item["tags"] = json.loads(item["tags"]) if item.get("tags") else []
                item["has_cloze"] = bool(item.get("has_cloze"))

                # Generate interval preview predictions for the 4 rating buttons
                state = ReviewState(
                    card_id=item["id"],
                    repetitions=item["repetitions"],
                    interval_days=item["interval_days"],
                    ease_factor=item["ease_factor"],
                    next_due=item["next_due"],
                )
                item["interval_previews"] = predict_intervals(state)
                queue.append(item)

            return queue

    def record_review(
        self, card_id: str, rating: int, response_time_ms: int = 0
    ) -> dict[str, Any]:
        """
        Processes a review of a card using SM-2 algorithm.
        rating: 1 (Nochmal), 2 (Schwer), 3 (Gut), 4 (Einfach)
        """
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                SELECT c.deck_id, r.*
                FROM cards c
                JOIN review_state r ON c.id = r.card_id
                WHERE c.id = ?
            """,
                (card_id,),
            )
            row = c.fetchone()
            if not row:
                raise ValueError(f"Card {card_id} not found.")

            deck_id = row["deck_id"]
            current_state = ReviewState(
                card_id=row["card_id"],
                repetitions=row["repetitions"],
                interval_days=row["interval_days"],
                ease_factor=row["ease_factor"],
                next_due=row["next_due"],
                last_reviewed=row["last_reviewed"],
                total_reviews=row["total_reviews"],
                lapses=row["lapses"],
                last_quality=row["last_quality"],
            )

            new_state, interval_days = calculate_sm2(current_state, rating)

            # Update review_state in DB
            c.execute(
                """
                UPDATE review_state
                SET repetitions = ?,
                    interval_days = ?,
                    ease_factor = ?,
                    next_due = ?,
                    last_reviewed = ?,
                    total_reviews = ?,
                    lapses = ?,
                    last_quality = ?
                WHERE card_id = ?
            """,
                (
                    new_state.repetitions,
                    new_state.interval_days,
                    new_state.ease_factor,
                    new_state.next_due,
                    new_state.last_reviewed,
                    new_state.total_reviews,
                    new_state.lapses,
                    new_state.last_quality,
                    card_id,
                ),
            )

            # Insert study_log entry
            c.execute(
                """
                INSERT INTO study_logs (card_id, deck_id, quality, interval_days, ease_factor, response_time_ms, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    card_id,
                    deck_id,
                    rating,
                    interval_days,
                    new_state.ease_factor,
                    response_time_ms,
                    new_state.last_reviewed,
                ),
            )
            conn.commit()

            return {
                "card_id": card_id,
                "state": new_state.to_dict(),
                "interval_days": interval_days,
                "next_due": new_state.next_due,
            }

    def reset_deck_progress(self, deck_id: str) -> bool:
        """Reset learning progress for all cards in a deck back to initial state."""
        now = utc_now_iso()
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                UPDATE review_state
                SET repetitions = 0,
                    interval_days = 0.0,
                    ease_factor = 2.5,
                    next_due = ?,
                    last_reviewed = NULL,
                    total_reviews = 0,
                    lapses = 0,
                    last_quality = NULL
                WHERE card_id IN (SELECT id FROM cards WHERE deck_id = ?)
            """,
                (now, deck_id),
            )
            conn.commit()
        return True

    # ==========================================
    # STATISTICS & ANALYTICS
    # ==========================================
    def get_stats(self) -> dict[str, Any]:
        now = utc_now()
        today_start = datetime(
            now.year, now.month, now.day, tzinfo=timezone.utc
        ).isoformat()

        with self.get_connection() as conn:
            c = conn.cursor()

            # Card counts
            c.execute("SELECT COUNT(*) FROM cards")
            total_cards = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM decks")
            total_decks = c.fetchone()[0]

            c.execute(
                """
                SELECT
                    SUM(CASE WHEN repetitions = 0 THEN 1 ELSE 0 END) as new_cards,
                    SUM(CASE WHEN repetitions BETWEEN 1 AND 2 THEN 1 ELSE 0 END) as learning_cards,
                    SUM(CASE WHEN repetitions >= 3 THEN 1 ELSE 0 END) as mastered_cards,
                    SUM(CASE WHEN next_due <= ? OR repetitions = 0 THEN 1 ELSE 0 END) as due_cards
                FROM review_state
            """,
                (now.isoformat(),),
            )
            counts = dict(c.fetchone())

            # Today's reviews
            c.execute(
                "SELECT COUNT(*), AVG(quality) FROM study_logs WHERE timestamp >= ?",
                (today_start,),
            )
            today_row = c.fetchone()
            reviews_today = today_row[0] or 0
            avg_quality_today = round(today_row[1], 2) if today_row[1] else 0.0

            # Total reviews and retention rate (rating >= 3 / total reviews)
            c.execute("""
                SELECT COUNT(*),
                       SUM(CASE WHEN quality >= 3 THEN 1 ELSE 0 END)
                FROM study_logs
            """)
            total_rev_row = c.fetchone()
            total_reviews = total_rev_row[0] or 0
            successful_reviews = total_rev_row[1] or 0
            retention_rate = (
                round((successful_reviews / total_reviews * 100), 1)
                if total_reviews > 0
                else 100.0
            )

            # Reviews in the last 14 days
            days_history = []
            for i in range(13, -1, -1):
                d = now - timedelta(days=i)
                d_start = datetime(
                    d.year, d.month, d.day, tzinfo=timezone.utc
                ).isoformat()
                d_end = (
                    datetime(d.year, d.month, d.day, tzinfo=timezone.utc)
                    + timedelta(days=1)
                ).isoformat()
                c.execute(
                    """
                    SELECT COUNT(*) FROM study_logs
                    WHERE timestamp >= ? AND timestamp < ?
                """,
                    (d_start, d_end),
                )
                cnt = c.fetchone()[0]
                days_history.append({"date": d.strftime("%d.%m."), "count": cnt})

            # Calculate study streak in days
            streak = 0
            check_date = now.date()
            c.execute(
                """
                SELECT COUNT(*) FROM study_logs
                WHERE timestamp >= ?
            """,
                (
                    datetime(
                        check_date.year,
                        check_date.month,
                        check_date.day,
                        tzinfo=timezone.utc,
                    ).isoformat(),
                ),
            )
            has_today = c.fetchone()[0] > 0
            if has_today:
                streak += 1
                curr = check_date - timedelta(days=1)
            else:
                curr = check_date - timedelta(days=1)

            while True:
                d_s = datetime(
                    curr.year, curr.month, curr.day, tzinfo=timezone.utc
                ).isoformat()
                d_e = (
                    datetime(curr.year, curr.month, curr.day, tzinfo=timezone.utc)
                    + timedelta(days=1)
                ).isoformat()
                c.execute(
                    "SELECT COUNT(*) FROM study_logs WHERE timestamp >= ? AND timestamp < ?",
                    (d_s, d_e),
                )
                if c.fetchone()[0] > 0:
                    streak += 1
                    curr -= timedelta(days=1)
                else:
                    break

            return {
                "total_cards": total_cards,
                "total_decks": total_decks,
                "new_cards": counts.get("new_cards") or 0,
                "learning_cards": counts.get("learning_cards") or 0,
                "mastered_cards": counts.get("mastered_cards") or 0,
                "due_cards": counts.get("due_cards") or 0,
                "reviews_today": reviews_today,
                "avg_quality_today": avg_quality_today,
                "total_reviews": total_reviews,
                "retention_rate": retention_rate,
                "study_streak": streak,
                "days_history": days_history,
            }

    # ==========================================
    # EXPORT & IMPORT
    # ==========================================
    def export_all(self) -> dict[str, Any]:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM decks")
            decks = [dict(r) for r in c.fetchall()]

            c.execute("SELECT * FROM cards")
            cards = []
            for r in c.fetchall():
                item = dict(r)
                item["tags"] = json.loads(item["tags"]) if item.get("tags") else []
                cards.append(item)

            c.execute("SELECT * FROM review_state")
            review_states = [dict(r) for r in c.fetchall()]

            return {
                "version": "1.0",
                "exported_at": utc_now_iso(),
                "decks": decks,
                "cards": cards,
                "review_state": review_states,
            }

    def import_all(self, data: dict[str, Any]) -> tuple[int, int]:
        """Imports decks and cards from exported JSON dictionary."""
        decks_imported = 0
        cards_imported = 0
        now = utc_now_iso()

        with self.get_connection() as conn:
            c = conn.cursor()
            for d in data.get("decks", []):
                c.execute(
                    """
                    INSERT OR REPLACE INTO decks (id, name, description, icon, color, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        d["id"],
                        d["name"],
                        d.get("description", ""),
                        d.get("icon", "atom"),
                        d.get("color", "#3b82f6"),
                        d.get("created_at", now),
                    ),
                )
                decks_imported += 1

            for card in data.get("cards", []):
                tags_json = json.dumps(card.get("tags", []), ensure_ascii=False)
                has_cloze = (
                    1
                    if ("{{" in card.get("front", "") or "{{" in card.get("back", ""))
                    else 0
                )
                c.execute(
                    """
                    INSERT OR REPLACE INTO cards (
                        id, deck_id, title, front, back, hint,
                        formula_breakdown, physical_meaning, validity_domain,
                        tags, difficulty, has_cloze, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        card["id"],
                        card["deck_id"],
                        card["title"],
                        card["front"],
                        card["back"],
                        card.get("hint", ""),
                        card.get("formula_breakdown", ""),
                        card.get("physical_meaning", ""),
                        card.get("validity_domain", ""),
                        tags_json,
                        card.get("difficulty", 3),
                        has_cloze,
                        card.get("created_at", now),
                        card.get("updated_at", now),
                    ),
                )
                cards_imported += 1

            # Restore review states if provided
            for r in data.get("review_state", []):
                c.execute(
                    """
                    INSERT OR REPLACE INTO review_state (
                        card_id, repetitions, interval_days, ease_factor, next_due, last_reviewed, total_reviews, lapses, last_quality
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        r["card_id"],
                        r.get("repetitions", 0),
                        r.get("interval_days", 0.0),
                        r.get("ease_factor", 2.5),
                        r.get("next_due", now),
                        r.get("last_reviewed"),
                        r.get("total_reviews", 0),
                        r.get("lapses", 0),
                        r.get("last_quality"),
                    ),
                )

            conn.commit()
        return decks_imported, cards_imported

    # ==========================================
    # SETTINGS STORAGE
    # ==========================================
    def get_setting(self, key: str, default: str | None = None) -> str | None:
        """Retrieves a configuration setting value by key."""
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = c.fetchone()
            return row["value"] if row else default

    def set_setting(self, key: str, value: str) -> None:
        """Saves or updates a configuration setting value."""
        now = utc_now_iso()
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO settings (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
            """,
                (key, value, now),
            )
            conn.commit()

    def delete_setting(self, key: str) -> bool:
        """Deletes a configuration setting by key."""
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM settings WHERE key = ?", (key,))
            conn.commit()
        return True

    def get_all_settings(self) -> dict[str, str]:
        """Returns all configuration settings as a dictionary."""
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT key, value FROM settings")
            rows = c.fetchall()
            return {r["key"]: r["value"] for r in rows}
