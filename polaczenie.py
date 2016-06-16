#! /usr/bin/env python2
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

sqlite_db = create_engine('sqlite:///E:\I sem\Orzechowski\projekt-z-gita\telemed')  # in RAM




mysql_db = create_engine('http://mysql.agh.edu.pl/phpMyAdmin/index.php', echo=True)
#pg_db = create_engine('postgres://login:password@localhost:5432/mydatabase', echo=True)
import sqlite3

# utworzenie połączenia z bazą przechowywaną na dysku
# lub w pamięci (':memory:')
con = sqlite3.connect('test.db')

# dostęp do kolumn przez indeksy i przez nazwy
con.row_factory = sqlite3.Row

# utworzenie obiektu kursora
cur = con.cursor()

