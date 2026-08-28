import mysql.connector
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME

def create_connection_mysql():
    """This function returns a connection object of MySQL by creating a connection"""
    db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    return db

def closing_connection_mysql(db_connection_object):
    """This function closes the created connection with MySQL"""
    db_connection_object.close()

def insert_user_details_db(db_connection_object, user_name, user_email, user_pass_hash):
    """This function inserts given details to the \"User\" table in database'"""
    cursor = db_connection_object.cursor()
    sql = ("INSERT INTO user (name, email, password_hash) values (%s, %s, %s)")
    values = (user_name, user_email, user_pass_hash)
    cursor.execute(sql, values)
    db_connection_object.commit()

def email_exists(db_connection_object, email):
    """This function checks that email exists in database or not"""
    cursor = db_connection_object.cursor()
    sql = "SELECT 1 FROM user WHERE email = %s"
    values = (email,)
    cursor.execute(sql, values)
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False

def retrieve_password_hash_from_email(db_connection_object, email):
    """This function returns the hash password from database using given email"""
    cursor = db_connection_object.cursor()
    sql = "SELECT password_hash FROM user WHERE email = %s"
    values = (email,)
    cursor.execute(sql, values)
    result = cursor.fetchone()
    return result
