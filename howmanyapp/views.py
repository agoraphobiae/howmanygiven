# what each page will look like

from howmanyapp import app
from flask import render_template, flash, redirect, request

from random import choice

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    msgs = ['Oops!', 'Doh!', 'Oh no!', 'Aw shucks.', 'Golly.', 'Damn']
    return render_template("404.html", 
        msg=choice(msgs)), 404