import mysql.connector
import os

def create_connection_mysql():
    db = mysql.connector.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"))
    return db

def closing_connection_mysql(db_connection_object):
    db_connection_object.close()

def insert_user_details_db(db_connection_object, user_name, user_email, user_pass_hash):
    cursor = db_connection_object.cursor()
    sql = ("INSERT INTO user (name, email, password_hash) values (%s, %s, %s)")
    values = (user_name, user_email, user_pass_hash)
    cursor.execute(sql, values)
    db_connection_object.commit()

def retrieve_password_hash_from_email(db_connection_object, email):
    cursor = db_connection_object.cursor()
    sql = "SELECT password_hash FROM user WHERE email = %s"
    values = (email,)
    cursor.execute(sql, values)
    result = cursor.fetchone()
    return result
