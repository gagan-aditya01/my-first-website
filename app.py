# app.py
import sqlite3
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DB = "family.db"

# ── Database Setup ────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                home INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS grocery (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL
            )
        """)
        existing = conn.execute("SELECT COUNT(*) FROM members").fetchone()[0]
        if existing == 0:
            conn.executemany(
                "INSERT INTO members (name, home) VALUES (?, ?)",
                [("Mom", 1), ("Dad", 0), ("Gagan", 1), ("Shashank", 0)]
            )
        conn.commit()

# ── Homepage ──────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ── Who's Home ────────────────────────────────────────────
@app.route("/api/members", methods=["GET"])
def get_members():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM members").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/members/<int:member_id>/toggle", methods=["POST"])
def toggle_member(member_id):
    with get_db() as conn:
        current = conn.execute(
            "SELECT home FROM members WHERE id = ?", (member_id,)
        ).fetchone()
        if not current:
            return jsonify({"error": "Member not found"}), 404
        new_status = 0 if current["home"] else 1
        conn.execute(
            "UPDATE members SET home = ? WHERE id = ?", (new_status, member_id)
        )
        conn.commit()
    return jsonify({"success": True, "home": new_status})

# ── Grocery List ──────────────────────────────────────────
@app.route("/api/grocery", methods=["GET"])
def get_grocery():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM grocery").fetchall()
        return jsonify([dict(r) for r in rows])

@app.route("/api/grocery", methods=["POST"])
def add_grocery():
    data = request.get_json()
    item = data.get("item", "").strip()
    if not item:
        return jsonify({"error": "Item cannot be empty"}), 400
    with get_db() as conn:
        cursor = conn.execute("INSERT INTO grocery (item) VALUES (?)", (item,))
        conn.commit()
        new_id = cursor.lastrowid
    return jsonify({"success": True, "id": new_id, "item": item})

@app.route("/api/grocery/<int:item_id>", methods=["DELETE"])
def delete_grocery(item_id):
    with get_db() as conn:
        conn.execute("DELETE FROM grocery WHERE id = ?", (item_id,))
        conn.commit()
    return jsonify({"success": True})

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
