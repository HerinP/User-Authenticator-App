import smtplib
from email.message import EmailMessage
import sys
from config import SERVER_HOST, SERVER_PORT, SCRIPT_EMAIL, SCRIPT_EMAIL_PASS

def write_email_message(otp, receiver_address):
    """This function creates a message object"""
    message = EmailMessage()
    message['Subject'] = "Verification Code"
    message['To'] = receiver_address
    message['From'] = SCRIPT_EMAIL
    message.set_content(f"Your OTP is {otp}")
    message.add_alternative(f"""<html>
    <h1>Verification Code</h1>
    <p>Your OTP is {otp}</p>
    </html>""", subtype= 'html')
    return message

def otp_by_email(message):
    """This function sents message to the recipient"""
    with smtplib.SMTP(host=SERVER_HOST,port=SERVER_PORT) as server:
        try:
            server.starttls()
            server.login(SCRIPT_EMAIL, SCRIPT_EMAIL_PASS)
            server.send_message(message)
            print("OTP sent to your email")
        except smtplib.SMTPRecipientsRefused:
            sys.exit("Some problem with your email.Try again...")
        except smtplib.SMTPSenderRefused:
            sys.exit("Some problem with our system responsible for sending mail")
        except smtplib.SMTPException as e:
            sys.exit(f"Some error occured {e}")