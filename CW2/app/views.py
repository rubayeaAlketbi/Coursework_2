from app import app
from flask import render_template, flash, redirect

@app.route('/')
def about():
    return render_template("about.html")