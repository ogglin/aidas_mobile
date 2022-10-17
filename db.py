import pymysql

from env import *


def _query(sql):
    result = []
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASS,
                                 database=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                result.append(row)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
        # print(result)
        return result
