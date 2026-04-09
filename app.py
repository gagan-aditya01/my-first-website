# app.py
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ─── Homepage ────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─── Who's Home ──────────────────────────────────────────
@app.route("/api/members", methods=["GET"])
def get_members():
    # Will be replaced with DB query in Step 5
    return jsonify([
        {"id": 1, "name": "Mom",  "home": True},
        {"id": 2, "name": "Dad",  "home": False},
        {"id": 3, "name": "Alex", "home": True},
        {"id": 4, "name": "Sam",  "home": False},
    ])

@app.route("/api/members/<int:member_id>/toggle", methods=["POST"])
def toggle_member(member_id):
    # Will be replaced with DB update in Step 5
    return jsonify({"success": True, "member_id": member_id})

# ─── Grocery List ─────────────────────────────────────────
@app.route("/api/grocery", methods=["GET"])
def get_grocery():
    return jsonify([
        {"id": 1, "item": "Milk"},
        {"id": 2, "item": "Eggs"},
        {"id": 3, "item": "Bread"},
    ])

@app.route("/api/grocery", methods=["POST"])
def add_grocery():
    data = request.get_json()
    item = data.get("item", "").strip()
    if not item:
        return jsonify({"error": "Item cannot be empty"}), 400
    return jsonify({"success": True, "item": item})

@app.route("/api/grocery/<int:item_id>", methods=["DELETE"])
def delete_grocery(item_id):
    return jsonify({"success": True, "item_id": item_id})

# ─── Run ─────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)