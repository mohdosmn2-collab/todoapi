"""Simple To-Do REST API built with Flask (in-memory storage)."""
import os

from flask import Flask, jsonify, request

app = Flask(__name__)

todos = []
next_id = 1


@app.route("/")
def home():
    return jsonify(message="Welcome to the To-Do API", version="1.0")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/todos", methods=["GET"])
def list_todos():
    return jsonify(todos)


@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify(error="'title' is required"), 400
    todo = {"id": next_id, "title": title, "done": False}
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json(silent=True) or {}
    for todo in todos:
        if todo["id"] == todo_id:
            todo["title"] = data.get("title", todo["title"])
            todo["done"] = data.get("done", todo["done"])
            return jsonify(todo)
    return jsonify(error="Todo not found"), 404


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return jsonify(message="Deleted")
    return jsonify(error="Todo not found"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
