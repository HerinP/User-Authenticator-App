import bcrypt
import sys
import re
import stdiomask

def register_login():
    """This function takes the user's choice to register or login or exit"""
    print("Enter 'REGISTER' if you want to register or 'LOGIN' if you want to login or 'Exit' if you want to exit: ", end='')
    while True:
        ask = input()
        if ask.lower() == 'register':
            return 'register'
        elif ask.lower() == 'login':
            return 'login' 
        elif ask.lower() == 'exit':
            sys.exit("Thankyou...")
        else:
            print("Enter 'REGISTER' or 'LOGIN' or 'Exit': ", end='')
    
def user_name():
    """This function returns the name by user input"""
    return input("Enter your name: ")

def user_email():
    """This function returns the email by user input"""
    return input("Enter your email: ")

def user_input_password():
    """This function returns the password by user input"""
    password = stdiomask.getpass("Enter Password: ", mask= "*")
    return password

def hash_password(password):
    """This function returns the hash password from the given password """
    pass_bytes = password.encode('UTF-8')
    salt_rounds = 12
    salt = bcrypt.gensalt(salt_rounds)
    hash_bytes = bcrypt.hashpw(pass_bytes, salt)
    hash_pass = hash_bytes.decode('UTF-8')
    return hash_pass

def verify_password(password1, password2):
    """This function returns the True if two password are same"""
    pass1 = password1.encode('UTF-8')
    pass2 = password2.encode('UTF-8')
    return bcrypt.checkpw(pass1, pass2)

def validate_email(email):
    pattern = r"[\w\.-]+@[\w\.-]+\.\w{2,}"
    match = re.fullmatch(pattern, email)
    return bool(match)