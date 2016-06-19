import os
from flask import Flask, render_template, redirect, request,url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics


app=Flask(__name__)


@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/baza")
def baza():
    return render_template('baza.html')

@app.route("/modify")
def modify():
    return render_template('modify.html')

@app.route("/add")
def add():
    return render_template('add.html')



app.run(debug=True)