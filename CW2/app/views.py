from app import app
from flask import render_template, flash, redirect

@app.route('/')
def home():
    return render_template("homepage.html")
