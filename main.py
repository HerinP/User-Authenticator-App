import secrets
import bcrypt
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import mysql.connector
import sys


def main():
    load_dotenv()
    register_or_login = register_login()
    if register_or_login == "register":
        user_input_name = user_name()
        user_input_email = user_email()
        otp = generate_otp()
        message = write_email_message(otp, user_input_email)
        otp_by_email(message)
        user_otp = int(input("Enter otp: "))
        if verify_otp(user_otp, otp):
            print("Verified!")
        else:
            sys.exit("Incorrect OTP!")
        user_password = user_input_password()
        user_hash_password = hash_password(user_password)
        object = create_connection_mysql()
        cursor = object.cursor()
        cursor.execute("USE authenticate_app")
        insert_user_details_db(object, user_input_name, user_input_email, user_hash_password)
        print("LOGGED IN!")
        closing_connection_mysql(object)
    else:
        user_input_email = user_email()
        object = create_connection_mysql()
        cursor = object.cursor()
        cursor.execute("USE authenticate_app")
        password_hash = retrieve_password_hash_from_email(object, user_input_email)
        if password_hash:
            user_password = user_input_password()
            if verify_password(user_password, password_hash[0]):
                print("LOGGED IN!") 
            else:
                print("WRONG PASSWORD!")
        else:
            sys.exit("No user was registered with this email.Try Registering! ")
        closing_connection_mysql(object)

def register_login():
    ask = input("Enter 'REGISTER' if you want to register or 'LOGIN' if you want to login. ")
    if ask.lower() == 'register':
        return 'register'
    elif ask.lower() == 'login':
        return 'login' 
    else:
        sys.exit("Enter 'REGISTER' or 'LOGIN'")
    
def user_name():
    return input("Enter your name: ")

def user_email():
    return input("Enter your email: ")

def generate_otp():
    otp = secrets.randbelow(900000) + 100000
    return otp

def verify_otp(user_input_otp, generated_otp):
    if secrets.compare_digest(str(user_input_otp), str(generated_otp)):
        return 1
    else:
        return 0

def user_input_password():
    password = input("Enter password: ")
    return password

def hash_password(password):
    pass_bytes = password.encode('UTF-8')
    salt_rounds = 12
    salt = bcrypt.gensalt(salt_rounds)
    hash_bytes = bcrypt.hashpw(pass_bytes, salt)
    hash_pass = hash_bytes.decode('UTF-8')
    return hash_pass

def verify_password(password1, password2):
    pass1 = password1.encode('UTF-8')
    pass2 = password2.encode('UTF-8')
    return bcrypt.checkpw(pass1, pass2)

def write_email_message(otp, receiver_address):
    message = EmailMessage()
    message['Subject'] = "Verification Code"
    message['To'] = receiver_address
    message['From'] = os.getenv("SCRIPT_EMAIL")
    message.set_content(f"Your OTP is {otp}")
    message.add_alternative(f"""<html>
    <h1>Verification Code</h1>
    <p>Your OTP is {otp}</p>
    </html>""", subtype= 'html')
    return message

def otp_by_email(message):
    with smtplib.SMTP(host=os.getenv("SERVER_HOST"),port=os.getenv("SERVER_PORT")) as server:
        server.starttls()
        server.login(os.getenv("SCRIPT_EMAIL"), os.getenv("SCRIPT_EMAIL_PASS"))
        server.send_message(message)

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

if __name__ == '__main__':
    main()