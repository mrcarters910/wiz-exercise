from flask import Flask, render_template_string, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
app = Flask(__name__)

# MongoDB connection string from environment variable
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/todo_app")
client = MongoClient(mongo_uri)
db = client.get_database()
todos = db.todos

TEMPLATE = """
<!doctype html>
<title>Wiz Todo App</title>
<h1>Todo List</h1>
<form method="post" action="/add">
  <input name="text" placeholder="New todo">
  <button type="submit">Add</button>
</form>
<ul>
  {% for todo in todos %}
    <li>
      {{ todo["text"] }}
      <form method="post" action="/delete/{{ todo["_id"] }}" style="display:inline;">
        <button type="submit">x</button>
      </form>
    </li>
  {% endfor %}
</ul>
"""

@app.route("/")
def index():
    all_todos = list(todos.find())
    return render_template_string(TEMPLATE, todos=all_todos)

@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if text:
        todos.insert_one({"text": text})
    return redirect("/")

@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect("/")

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
