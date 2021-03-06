import os
from flask import Flask, render_template, redirect, request,url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import statistics
from datetime import datetime
import cgi
import numpy

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

@app.route("/modify", methods=['POST'])
def modify():
    data = Data.query.filter(Data.id==request.form['id'])
    data=data.first()
    return render_template('modify.html', data=data)

@app.route("/save_changes", methods=['POST'])
def save_changes():
    data = Data.query.filter(Data.id==request.form['id'])
    data = data.first()
    if(request.form['patient_id']!=""):
        data.patient_id=request.form['patient_id']
    if(request.form['name']!=""):
        data.name=request.form['name'].upper()
    if(request.form['surname']!=""):
        data.surname=request.form['surname'].upper()
    if(request.form['activity']!=""):
        data.activity=request.form['activity'].upper()
    signals_db.session.commit()
    return render_template('changed.html', data=data)

@app.route("/add")
def add():
    return render_template('add.html')

@app.route("/download", methods = ['POST'])
def download():
    data = Data.query.filter(Data.id==request.form['id'])
    signal = Signal.query.filter(Signal.data_id==request.form['id'])
    data = data.first()
    input = str(data.patient_id) + "," + data.activity + "," + data.name + "," + data.surname + "\nCZAS,aX,aY,taZ\n"
    for element in signal:
        input = input + str(element.time) + "," + str(element.aX) +"," + str(element.aY) + "," + str(element.aZ) + "\n"
    f = open(data.activity.lower() + "_" + data.name.lower() + "_" + data.surname.lower() + '.csv', 'w')
    f.write(input)
    f.close()
    return redirect('/baza')

@app.route("/save", methods=['GET', 'POST'])
def save():
    file=request.files['file']
    # nagłówek
    header = file.readline().decode('utf-8').split()

    patient_data = Data(header[0], header[2], header[3], header[1])
    signals_db.session.add(patient_data)
    signals_db.session.commit()

    file.readline()

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



    meanX = round(numpy.mean(aX),2)
    meanY = round(numpy.mean(aY),2)
    meanZ = round(numpy.mean(aZ),2)

    stdX = round(numpy.std(aX),2)
    stdY = round(numpy.std(aX),2)
    stdZ = round(numpy.std(aX),2)

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

    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('signal.html',
                           ids=ids,
                           graphJSON=graphJSON,
                           meanX = meanX,
                           meanY = meanY,
                           meanZ = meanZ,
                           stdX = stdX,
                           stdY = stdY,
                           stdZ = stdZ,
                           lenX = round(len(aX)/250,2),
                           lenY = round(len(aY)/250,2),
                           lenZ = round(len(aZ)/250,2),
                                        )

app.run(debug=True)