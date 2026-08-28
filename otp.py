import secrets
from inputimeout import inputimeout, TimeoutOccurred

def generate_otp():
    """This function generates a random 6-Digits number"""
    END_AT = 900000
    SUM_UP = 100000
    otp = secrets.randbelow(END_AT) + SUM_UP
    return otp

def time_limit_input(timeout):
    """This function waits for user to input for a limited time"""
    try:
        return int(inputimeout("Enter otp: ", timeout))
    except ValueError:
        print("OTPs are in Integer format!")
    except TimeoutOccurred:
        print("OTP expired")

def verify_otp(user_input_otp, generated_otp):
    """This function verifies the generated otp and user input otp"""
    return secrets.compare_digest(str(user_input_otp), str(generated_otp))