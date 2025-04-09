# imports
import random
import string

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# My App
app = Flask(__name__)

app.config

@app.route('/') # run index when someone goes to this url (root) 
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) # run the app in debug mode