import smtplib
from email.message import EmailMessage
import sys
from config import SERVER_HOST, SERVER_PORT, SCRIPT_EMAIL, SCRIPT_EMAIL_PASS

def email_otp_message(otp, receiver_address):
    """This function creates a message object"""
    message = EmailMessage()
    message['Subject'] = "Verification Code"
    message['To'] = receiver_address
    message['From'] = SCRIPT_EMAIL
    message.set_content(f"Your OTP is {otp}")
    message.add_alternative(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <title>Your One-Time Password</title>
</head>
<body>
  <h2>Your One-Time Password</h2>
  <p>Hello,</p>
  <p>Use the following one-time password (OTP) to complete your verification:</p>
  <h1>{otp}</h1>
  <p>This OTP is valid for 3 minutes and can be used only once.</p>
  <p>For your security, do not share this code with anyone. Our team will never ask you for your OTP.</p>
  <p>If you did not request this code, please ignore this email or contact our support team.</p>
  <p>Thank you.</p>
</body>
</html>""", subtype= 'html')
    return message

def email_otp_sending(message):
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