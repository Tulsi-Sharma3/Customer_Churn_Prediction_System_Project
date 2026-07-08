import mysql.connector
db = mysql.connector.connect(host="localhost",user="root",password="4567")
if db:
    print("connect successfully")
else:
    print("not")
dbCursor = db.cursor()
dbCursor.execute("create database tulsi;")
dbCursor.execute("show databases;")
# %s= placeholder mean
# executemany() = insert all row in command
db.commit()
'''
import install pandassql
'''