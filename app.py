# imports
import random
import string
import validators

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
    return render_template('index.html', error=None)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url'].strip()

    # Normalize URL
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url

    # Validate URL
    if not validators.url(original_url):
        return render_template('index.html', error="Invalid URL")

    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()

        # Check if the URL already exists
        cursor.execute("SELECT short_code FROM urls WHERE original_url = ?", (original_url,))
        row = cursor.fetchone()
        if row:
            short_code = row[0]
        else:
            # Generate a unique short code
            while True:
                short_code = generate_short_code()
                cursor.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,))
                if not cursor.fetchone():
                    break

            # Insert into DB
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

init_db() # gunicorn doesnt run main - run for when site is live
if __name__ == '__main__':
    init_db() # initialize the database when the app starts - for local development
    app.run(debug=True) # run the app in debug mode
