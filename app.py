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

if __name__ == '__main__':
    init_db() # initialize the database when the app starts
    app.run(debug=True) # run the app in debug mode
