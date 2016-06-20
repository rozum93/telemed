import os
from flask import Flask, render_template, redirect, request,url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics
import cgi


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

signals_db = SQLAlchemy(app)

class Data(signals_db.Model):
    __tablename__ = 'data'
    id = signals_db.Column(signals_db.Integer, primary_key=True)

    # tam jest jakieś patient_id, które jest tekstem, więc tak to dodałam
    patient_id = signals_db.Column(signals_db.String)
    name = signals_db.Column(signals_db.String)
    surname = signals_db.Column(signals_db.String)
    activity = signals_db.Column(signals_db.String)
    sampling_freq = signals_db.Column(signals_db.Integer)

    signals = signals_db.relationship("Signal", backref="data", lazy="dynamic")

    def __init__(self, patient_id, name, surname, activity, sampling_freq):
        self.patient_id=patient_id
        self.name=name
        self.surname=surname
        self.activity=activity
        self.sampling_freq=sampling_freq

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

@app.route("/baza")
def baza():
    data = signals_db.session.query(Data).all()
    signals = signals_db.session.query(Signal).all()
    for element in signals:
        print(str(element.id) + "\t" + str(element.data_id) + "\t" + str(element.time) + "\t" + str(element.aX) + "\t" + str(element.aY) + "\t" + str(element.aZ))
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
    patient_data = Data(header[0], header[2], header[3], header[1], 0.5)
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




app.run(debug=True)