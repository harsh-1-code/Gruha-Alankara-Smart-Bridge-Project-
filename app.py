from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from models import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')

@app.route('/ar-viewer')
def ar_viewer():
    return render_template('ar_viewer.html')

@app.route('/live-ar-camera')
def live_ar_camera():
    return render_template('live_ar_camera.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
