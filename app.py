# app.py

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os


app = Flask(__name__)
CORS(app)

DB_PATH = "goldenkey.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            visit_date TEXT,
            source TEXT,
            notes TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/submit_lead", methods=["POST"])
def submit_lead():
    data = request.get_json()
    name = data.get("name")
    phone = data.get("phone")
    email = data.get("email", "")
    visit_date = data.get("visit_date", "")
    source = data.get("source", "Website")
    notes = data.get("notes", "")

    if not name or not phone:
        return jsonify({"status": "error", "message": "Name and phone required"}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO leads (name, phone, email, visit_date, source, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (name, phone, email, visit_date, source, notes, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Lead stored successfully!"})
@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Golden Key Apartments</title>
        </head>
        <body style='font-family:Arial;text-align:center;margin-top:50px;'>
            <h1>Welcome to Golden Key Apartments</h1>
            <p>Submit your enquiry <a href="/enquiry">here</a></p>
        </body>
    </html>
    """



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

