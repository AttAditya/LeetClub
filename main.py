from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS
from logging import getLogger, _nameToLevel

from modules import leetcode, read_file, database

getLogger("werkzeug").setLevel(_nameToLevel["ERROR"])

app = Flask(
    __name__,
    static_folder="res",
    static_url_path="/res"
)

CORS(app)

@app.route("/")
def index():
    return read_file()

@app.route("/refresh")
def refresh():
    results = database.databases["users"].fetch()
    all_items = results.items

    while results.last:
        results = database.databases["users"].fetch(last=results.last)
        all_items += results.items
    
    users = [item["key"] for item in all_items]
    data = {user: leetcode.data(user) for user in users}

    for user, stats in data.items():
        database.databases["stats"].put(stats, user)

    return jsonify({"message": "Refreshed."})

@app.route("/api/users")
def users():
    results = database.databases["stats"].fetch()
    all_items = results.items

    while results.last:
        results = database.databases["users"].fetch(last=results.last)
        all_items += results.items

    data = results.items
    data.sort(key=lambda x: (
        x["streak"],
        x["rating"],
        x["questionCount"]
    ), reverse=True)

    return jsonify(data)

@app.route("/user/<username>")
@app.route("/api/users/<username>")
def user(username):
    user_data: Any = database.databases["stats"].get(username)
    existing_data: Any = database.databases["stats"].get(username)
    
    if existing_data:
        user_data["streak"] = existing_data["streak"]
    
    if not user_data:
        user_data = leetcode.data(username)
        database.databases["users"].put({"permissions": []}, username)
        database.databases["stats"].put(user_data, username)

    return jsonify(user_data)

@app.route("/user/<username>/refresh")
@app.route("/api/users/<username>/refresh")
def user_refresh(username):
    user_data = leetcode.data(username)
    existing_data: Any = database.databases["stats"].get(username)
    
    if existing_data:
        user_data["streak"] = existing_data["streak"]
    
    database.databases["stats"].put(user_data, username)

    return jsonify(user_data)

@app.route("/user/<username>/streak", methods=["POST"])
@app.route("/api/users/<username>/streak", methods=["POST"])
def user_streak(username):
    data = request.get_json()
    
    streak = data.get("streak", 0)
    user_data: Any = database.databases["stats"].get(username)
    
    if not user_data:
        return jsonify({"message": "User not found."}), 404
    
    user_data["streak"] = int(streak)
    database.databases["stats"].put(user_data, username)

    return jsonify(user_data)

if __name__ == "__main__":
    config: dict = {
        "host": "0.0.0.0",
        "port": 4201
    }

    app.run(**config)

