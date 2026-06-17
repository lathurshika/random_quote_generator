from flask import Flask, render_template
import sqlite3
import random
import os

app = Flask(__name__)

DATABASE = "quotes.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT NOT NULL,
        author TEXT NOT NULL
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM quotes")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_quotes = [
            ("The future depends on what you do today.", "Mahatma Gandhi"),
            ("Stay hungry, stay foolish.", "Steve Jobs"),
            ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
            ("Success is not final, failure is not fatal.", "Winston Churchill"),
            ("Dream big and dare to fail.", "Norman Vaughan"),
            ("Do what you can, with what you have, where you are.", "Theodore Roosevelt"),
            ("Everything you can imagine is real.", "Pablo Picasso"),
            ("Act as if what you do makes a difference. It does.", "William James")
        ]

        cursor.executemany(
            "INSERT INTO quotes (quote, author) VALUES (?, ?)",
            sample_quotes
        )

    conn.commit()
    conn.close()

def get_random_quote():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT quote, author FROM quotes")
    quotes = cursor.fetchall()

    conn.close()

    return random.choice(quotes)

@app.route("/")
def home():
    quote, author = get_random_quote()
    return render_template(
        "index.html",
        quote=quote,
        author=author
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)