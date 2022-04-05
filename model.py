import mysql.connecter
from mysql.connecter import Error

def create_connection(host_name, user_name, user_password, db_name): 
   connection = None 
   try: 
      connection=mysql.connector.connect(
         host=host_name, 
         user=user_name,                      
         passwd=user_password,   
         database=db_name 
      ) 
      print("Connection to MySQL DB successful") 
   except Error as e: 
      print(f"The error '{e}' occurred") 
   return connection 

def execute_query(connection, query,**add): 
   cursor = connection.cursor() 
   try:  
      if len(add) == 0:
         cursor.execute(query)  
         connection.commit() 
         print("Query executed successfully")          
      else:
         cursor.execute(query,add)  
         connection.commit() 
         print("Query executed successfully")          
   except Error as e: 
      print(f"The error '{e}' occurred") 

def createTable(mes):
   boom = f"""
CREATE TABLE IF NOT EXISTS chat_{mes}(
   id_st INT,
   fname TEXT NOT NULL,
   sname TEXT NOT NULL,
   score INT NOT NULL,
   username TEXT NOT NULL,
   PRIMARY KEY (id_st)
) ENGINE = InnoDB"""
   return execute_query(connection, boom)

def insertStudent(id_c1,fname1,sname1,score1,username1):
   boom = f"""
INSERT INTO
  `users` (`id_st`, `fname`, `sname`, `score`,`username`)
VALUES
  (%(id_c)i, %(fname)s, %(sname)s, %(score)i,%(username)s)
"""
   return execute_query(connection, boom,id_c=id_c1,fname=fname1,sname=sname1,score=score1,username=username1)

def updateScore(mes,id_c1,score1):
   update_post_description = f"""
   UPDATE
     chat_{mes}
   SET
     score = %(score)i
   WHERE
     id_st = %(id_c)i
   """
   return execute_query(connection, update_post_description,score=score1,id_c=id_c1)   
def getStudents(mes):
   select_users_posts = f"""
   SELECT
     *
   FROM
     chat_{mes}
   """
   return execute_query(connection, select_users_posts)   