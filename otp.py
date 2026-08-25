import secrets
from inputimeout import inputimeout, TimeoutOccurred

def generate_otp():
    otp = secrets.randbelow(900000) + 100000
    return otp

def time_limit_input(timeout):
    try:
        return int(inputimeout("Enter otp: ", timeout))
    except TimeoutOccurred:
        print("OTP expired")

def verify_otp(user_input_otp, generated_otp):
    if secrets.compare_digest(str(user_input_otp), str(generated_otp)):
        return 1
    else:
        return 0