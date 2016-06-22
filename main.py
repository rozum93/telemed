import os
from flask import Flask, render_template, redirect, request,url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import statistics
from datetime import datetime
import cgi

import json
import plotly

import pandas as pd
import numpy as np



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

signals_db = SQLAlchemy(app)

class Data(signals_db.Model):
    __tablename__ = 'data'
    id = signals_db.Column(signals_db.Integer, primary_key=True)

    # tam jest jakieś patient_id, które jest tekstem, więc tak to dodałam
    patient_id = signals_db.Column(signals_db.Integer)
    name = signals_db.Column(signals_db.String)
    surname = signals_db.Column(signals_db.String)
    activity = signals_db.Column(signals_db.String)

    signals = signals_db.relationship("Signal", backref="data", lazy="dynamic")

    def __init__(self, patient_id, name, surname, activity):
        self.patient_id=patient_id
        self.name=name
        self.surname=surname
        self.activity=activity

class Signal(signals_db.Model):
    __tablename__ = 'signal'
    id = signals_db.Column(signals_db.Integer, primary_key=True)
    data_id = signals_db.Column(signals_db.Integer, signals_db.ForeignKey("data.id"))
    time = signals_db.Column(signals_db.Integer)
    aX = signals_db.Column(signals_db.Integer)
    aY = signals_db.Column(signals_db.Integer)
    aZ = signals_db.Column(signals_db.Integer)

    def __init__(self, data_id, time, aX, aY, aZ):
        self.data_id=data_id
        self.time=time
        self.aX=aX
        self.aY=aY
        self.aZ=aZ

signals_db.create_all()

@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/baza", methods=['GET', 'POST'])
def baza():
    if request.method=='GET':
        data = signals_db.session.query(Data).all()
    else:
        to_find = request.form['enter_string']
        if request.form['search_by']=='activity':
            data = Data.query.filter(Data.activity.ilike('%'+to_find+'%'))
        elif request.form['search_by']=='patient_id':
            data = Data.query.filter(Data.patient_id==to_find)
        elif request.form['search_by']=='surname':
            data = Data.query.filter(Data.surname.ilike('%'+to_find+'%'))


    return render_template('baza.html', data=data)

@app.route("/modify")
def modify():
    return render_template('modify.html')

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/save", methods=['GET', 'POST'])
def save():
    file=request.files['file']
    # nagłówek
    header = file.readline().decode('utf-8').split()

    # wpisywanie nagłówka do bazy - sampling frequency na razie stałe, bo nie wiem jakie było
    patient_data = Data(header[0], header[2], header[3], header[1])
    signals_db.session.add(patient_data)
    signals_db.session.commit()

    # pozbywamy się linijki "CZAS aX aY aZ" i pierwszego rekordu niestety :(  bo jest w tej samej linijce. to trzeba poprawić
    print(file.readline())

    # czytanie sygnału
    for line in file:
        signal = line.decode('utf-8').split()
        if signal != []:
            element = Signal(patient_data.id, signal[0], signal[1], signal[2], signal[3])
            signals_db.session.add(element)
        else:
            break

    signals_db.session.commit()
    return redirect('/')

@app.route("/signal", methods=['POST'])
def signal():

    rng = pd.date_range('1/1/2011', periods=7500, freq='H')
    ts = pd.Series(np.random.randn(len(rng)), index=rng)

    signals = Signal.query.filter(Signal.data_id==request.form['id'])
    time = []
    aX = []
    aY = []
    aZ = []

    for element in signals:
        time = time+[element.time]
        aX = aX+[element.aX]
        aY = aY+[element.aY]
        aZ = aZ+[element.aZ]

    graphs = [
        dict(
            data=[
                dict(
                    x=time,
                    y=aX,
                    type='scatter',
                    name='przyspieszenie w osi X'
                ),
                dict(
                    x=time,
                    y=aY,
                    type='scatter',
                    name='przyspieszenie w osi Y'
                ),
                dict(
                    x=time,
                    y=aZ,
                    type='scatter',
                    name='przyspieszenie w osi Z'
                )
            ],
            layout=dict(
                title='Wykres przyspieszenia w trzech osiach'
            )
        ),
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('signal.html',
                           ids=ids,
                           graphJSON=graphJSON)

app.run(debug=True)