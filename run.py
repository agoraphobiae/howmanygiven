from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import config

# startup
# this will also load config.py down the line
from howmanyapp import app

app.run(debug = config.DEBUG)