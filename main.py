import secrets

def main():
    pass

def user_details():
    user_name = input("Enter your name: ")
    user_email = input("Enter your email: ")
    user_details_list = [user_name, user_email]
    return user_details_list

def generate_otp():
    otp = secrets.randbelow(900000) + 100000
    return otp
