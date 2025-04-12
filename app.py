# imports
import random
import string

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# initialize database
def init_db():
    with sqlite3.connect("urls.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                click_count INTEGER DEFAULT 0
            )
        ''')

# My App
app = Flask(__name__)

app.config

@app.route('/') # run index when someone goes to this url (root) 
def index():
    return render_template('index.html')

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url']
    short_code = generate_short_code()

    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)", (original_url, short_code))
        conn.commit()

    short_url = request.host_url + short_code
    return render_template('index.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_original(short_code):
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
        result = cursor.fetchone()

    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404


if __name__ == '__main__':
    init_db() # initialize the database when the app starts
    app.run(debug=True) # run the app in debug mode
