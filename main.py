import secrets
import bcrypt

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