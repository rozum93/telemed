from sqlalchemy import create_engine

sqlite_db = create_engine('sqlite:///E:\I sem\Orzechowski\projekt-z-gita\telemed')  # in RAM


#sqlite_db = create_engine('sqlite:////absolute/path/to/database.foo', echo=True) # absolute path for SQLite
#sqlite_db = create_engine('sqlite:///db.sqlite', echo=True) # relative path

#mysql_db = create_engine('mysql://localhost/database_name', echo=True)
#pg_db = create_engine('postgres://login:password@localhost:5432/mydatabase', echo=True)