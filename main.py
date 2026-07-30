import secrets
import bcrypt
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import mysql.connector


def main():
    load_dotenv()

def user_details():
    user_name = input("Enter your name: ")
    user_email = input("Enter your email: ")
    user_details_list = [user_name, user_email]
    return user_details_list

def generate_otp():
    otp = secrets.randbelow(900000) + 100000
    return otp

def verify_otp(user_input_otp, generated_otp):
    if secrets.compare_digest(user_input_otp, generated_otp):
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
    cursor = db.cursor()
    return [db, cursor]

def closing_connection_mysql(db_connection_object):
    db_connection_object.close()
