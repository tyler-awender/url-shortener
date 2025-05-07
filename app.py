"""
URL Shortener Web Application

This is a Flask-based URL shortener that takes long URLs and generates shorter and more managable links.
It uses SQLite as a backend to store URL mappings, timestamps.

Shortened URLs are handled through dynamic routing and user history is managed client side through the browser's 'localStorage'

Authors: Tyler Awender, Jugraj Pander, John Buclatin
"""

# Standard imports
import random
import string
import validators

# Third party imports
from flask import Flask, render_template, request, redirect
import sqlite3

# --------------
# DATABASE SETUP
# --------------

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

# -----------------
# UTILITY FUNCTIONS
# ------------------
def generate_short_code(length=6):
    """
    Generates a random alphanumeric short code of 6 char.
    Short code is used to represent the original URL

    Returns:
        str: A randomly generated short code
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# -------
# ROUTES
# -------

@app.route('/') 
def index():
    """
    Handles GET requests to root URL
    Renders homepage

    Returns:
        Rendered HTML template of home page
    """
    return render_template('index.html', error=None)

@app.route('/shorten', methods=['POST'])
def shorten():
    """
    Handles form submissions for shortening
    - normalizes URL
    - validates URL
    - checks DB for existing mappings
    - if new, stores a new mapping with new short code

    Returns:
        Rendered HTML template with shortened URL or error message
    """
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
    """
    Redirects users from the shortened URL to the original URL
    If no match is found, return a 404 error

    Returns:
        A redirect to the original URL or 404 error page
    """
    with sqlite3.connect("urls.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
        result = cursor.fetchone()

    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404


#---------------
# APP ENTRYPOINT
#----------------

# init database before app starts(for live deployment)
init_db() 
if __name__ == '__main__':
    init_db() # initialize the database when the app starts - for local development
    app.run(debug=True)
