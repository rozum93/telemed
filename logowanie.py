import pymysql


# Connect to the database
connection = pymysql.connect(host='mysql.agh.edu.pl',
                             user='olgaj',
                             password='DAmNw1yX',
                             db='olgaj',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `tbl_users` (`username`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `userid`, `password` FROM `tbl_users` WHERE `username`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()