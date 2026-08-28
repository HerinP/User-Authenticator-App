from dotenv import load_dotenv
import sys
from auth import register_login, user_name, user_email, user_input_password, verify_password, hash_password, validate_email, user_input_confirm_password
from database import create_connection_mysql, closing_connection_mysql, insert_user_details_db,email_exists, retrieve_password_hash_from_email
from email_service import write_email_message, otp_by_email
from otp import generate_otp, verify_otp, time_limit_input

def main():
    try:
        conn_obj = create_connection_mysql()
        cursor = conn_obj.cursor()
        cursor.execute("USE authenticate_app")
        register_or_login = register_login()
        if register_or_login == "register":
            user_input_name = user_name()
            if user_input_name is None:
                sys.exit("Enter a valid name")
            user_input_email = user_email()
            if validate_email(user_input_email) == False:
                sys.exit("Enter a valid Email")
            if email_exists(conn_obj, user_input_email):
                sys.exit("This email is already registered!")
            OTP_TIME_LIMIT = 180
            while True:
                otp = generate_otp()
                message = write_email_message(otp, user_input_email)
                otp_by_email(message)
                user_otp = time_limit_input(OTP_TIME_LIMIT)
                if user_otp is not None:
                    if verify_otp(user_otp, otp):
                        print("Verified!")
                        break
                    else:
                        print("Incorrect OTP!")
                resend = input("Enter 'Resend' to send a new verification code: ")
                if resend.lower() != 'resend':
                    sys.exit()
            user_password = user_input_password()
            if user_input_confirm_password(user_password) == False:
                sys.exit("Passwords don't match!")
            user_hash_password = hash_password(user_password)
            
            insert_user_details_db(conn_obj, user_input_name, user_input_email, user_hash_password)
            print("LOGGED IN!")
            closing_connection_mysql(conn_obj)
        else:
            user_input_email = user_email()
            if validate_email(user_input_email) == False:
                sys.exit("Enter a valid Email")
            password_hash = retrieve_password_hash_from_email(conn_obj, user_input_email)
            if password_hash:
                user_password = user_input_password()
                if verify_password(user_password, password_hash[0]):
                    print("LOGGED IN!") 
                else:
                    print("WRONG PASSWORD!")
            else:
                sys.exit("No user was registered with this email.Try Registering! ")
    finally:
        closing_connection_mysql(conn_obj)

if __name__ == '__main__':
    main()