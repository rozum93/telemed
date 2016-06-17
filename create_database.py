from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
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
    samplig_freq = signals_db.Column(signals_db.Integer)

    signals = signals_db.relationship("Signal", backref="data", lazy="dynamic")

    def __init__(self, patient_id, name, surname, activity, samplig_freq):
        self.patient_id=patient_id
        self.name=name
        self.surname=surname
        self.activity=activity
        self.samplig_freq=samplig_freq

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

# dodawanie sygnału do bazy
file_object = open('44_DANE.TXT')

# nagłówek
header = file_object.readline().split()

# wpisywanie nagłówka do bazy - sampling frequency na razie stałe, bo nie wiem jakie było
patient_data = Data(header[0], header[2], header[3], header[1], 0.5)
signals_db.session.add(patient_data)
signals_db.session.commit()

# pozbywamy się linijki "CZAS aX aY aZ" i pierwszego rekordu niestety :(  bo jest w tej samej linijce. to trzeba poprawić
print(file_object.readline())

# czytanie sygnału
for line in file_object:
    signal = line.split()
    element = Signal(patient_data.id, signal[0], signal[1], signal[2], signal[3])
    signals_db.session.add(element)

signals_db.session.commit()

# dla potwierdzenia wydruk tego co jest w bazie
header_list = signals_db.session.query(Data).all()
for el in header_list:
    print(str(el.id) + " " + el.patient_id + " " + el.name + " " + el.surname + " " + el.activity + " " + str(el.samplig_freq))
fd_list = signals_db.session.query(Signal).all()
for el in fd_list:
    print(str(el.id) + " " + str(el.data_id) + " " + str(el.time) + " " + str(el.aX) + " " + str(el.aY) + " " + str(el.aZ))