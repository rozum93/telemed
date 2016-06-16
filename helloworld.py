from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# baza dla klas tabel
Base = declarative_base()

# przykładowa klasa mapująca tabelę z bazy danych
class User(Base):
  __tablename__ = 'users'

  # pola i ich typy
  id = Column(Integer, primary_key=True)
  name = Column(String)
  fullname = Column(String)
  password = Column(String)

  def __init__(self, name, fullname, password):
      self.name = name
      self.fullname = fullname
      self.password = password

  def __repr__(self):
     return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)