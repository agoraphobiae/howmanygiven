# what each page will look like

from howmanyapp import app
from flask import render_template, flash, redirect, request
from howmany import *

from random import choice
from urlparse import urlparse

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/fuck/<path>')
def countf(path):
    print "PATH", path
    if urlparse(path).scheme == '':
        path = "http://" + path
    return render_template("fquery.html", 
        count=count_in_page(path, 'fuck'),
        queryurl=path)

@app.route('/<path:path>')
def analyze(path):
    print "PATH", path
    if urlparse(path).scheme == '':
        path = "http://" + path
    return render_template("query.html",
        queryname=cleanQueryName(path),
        data=analyze_page(path))

@app.errorhandler(404)
def page_not_found(e):
    msgs = ['Oops!', 'Doh!', 'Oh no!', 'Aw shucks.', 'Golly.', 'Damn']
    return render_template("404.html", 
        msg=choice(msgs)), 404