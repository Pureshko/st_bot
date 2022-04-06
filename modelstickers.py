import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path,check_same_thread=False)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return f"The error '{e}' occurred"
def execute_query(connection, query, *add):
    cursor = connection.cursor()
    try:
        if len(add)==0:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        elif len(add)==2:
            cursor.execute(query,(add[0],add[1]))
            connection.commit()
            print("Query executed successfully")
        elif len(add)==3:
            cursor.execute(query,(add[0],add[1],add[2]))
            connection.commit()
            print("Query executed successfully")
        elif len(add)==5:
            cursor.execute(query,(add[0],add[1],add[2],add[3],add[4]))
            connection.commit()
            print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        return f"The error '{e}' occurred"

def createTable(connection,mes):
    mes = str(mes)
    if "-" in mes:
        boom = f"""
        CREATE TABLE IF NOT EXISTS chat_{mes[1:len(mes)]}(
            id_st INTEGER PRIMARY KEY,
            fname TEXT NOT NULL,
            sname TEXT NOT NULL,
            score INTEGER NOT NULL,
            username TEXT NOT NULL
        );"""
        return execute_query(connection, boom)
    else:
        boom = f"""
        CREATE TABLE IF NOT EXISTS chat_{mes}(
            id_st INTEGER PRIMARY KEY,
            fname TEXT NOT NULL,
            sname TEXT NOT NULL,
            score INTEGER NOT NULL,
            username TEXT NOT NULL
        );"""
        return execute_query(connection, boom)

def insertStudent(connection,mes,id_c1,fname1,sname1,score1,username1):
    mes = str(mes)
    if "-" in mes:
        boom = f"""
        INSERT OR IGNORE INTO
            chat_{mes[1:len(mes)]} (`id_st`, `fname`, `sname`, `score`,`username`)
        VALUES
            (?,?,?,?,?)
        """
        return execute_query(connection,boom,id_c1,fname1,sname1,score1,username1)
    else:
        boom = f"""
        INSERT OR IGNORE INTO
            chat_{mes} (`id_st`, `fname`, `sname`, `score`,`username`)
        VALUES
            (?,?,?,?,?)
        """
        return execute_query(connection,boom,id_c1,fname1,sname1,score1,username1)

def updateName(connection,mes,id_c1,fname1,sname1):
    mes = str(mes)
    if "-" in mes:
        update_post_description = f"""
        UPDATE
          chat_{mes[1:len(mes)]}
        SET
           fname = ?,
           sname = ?
        WHERE
           id_st = ?
        """
        return execute_query(connection, update_post_description,fname1,sname1,id_c1)
    else:
        update_post_description = f"""
        UPDATE
          chat_{mes}
        SET
           fname = ?,
           sname = ?
        WHERE
           id_st = ?
        """
        return execute_query(connection, update_post_description,fname1,sname1,id_c1)


def updateScore(connection,mes,id_c1,score1):
    mes = str(mes)
    if "-" in mes:
        update_post_description = f"""
        UPDATE
          chat_{mes[1:len(mes)]}
        SET
          score = ?
        WHERE
           id_st = ?
        """
        return execute_query(connection, update_post_description,score1,id_c1)
    else:
        update_post_description = f"""
        UPDATE
          chat_{mes}
        SET
          score = ?
        WHERE
           id_st = ?
        """
        return execute_query(connection, update_post_description,score1,id_c1)


def getStudents(connection,mes):
    mes = str(mes)
    if "-" in mes:
        select_users_posts = f"""
        SELECT
          *
        FROM
          chat_{mes[1:len(mes)]}
        """
        return execute_read_query(connection, select_users_posts)
    else:
        select_users_posts = f"""
        SELECT
          *
        FROM
          chat_{mes}
        """
        return execute_read_query(connection, select_users_posts)
