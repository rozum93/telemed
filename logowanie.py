from sqlalchemy import create_engine

sqlite_db = create_engine('sqlite:///E:\I sem\Orzechowski\projekt-z-gita\telemed')  # in RAM




#mysql_db = create_engine('http://mysql.agh.edu.pl/phpMyAdmin/index.php', echo=True)
#pg_db = create_engine('postgres://login:password@localhost:5432/mydatabase', echo=True)