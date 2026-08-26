from dotenv import load_dotenv
import sys
from auth import register_login, user_name, user_email, user_input_password, verify_password, hash_password
from database import create_connection_mysql, closing_connection_mysql, insert_user_details_db,email_exists, retrieve_password_hash_from_email
from email_service import write_email_message, otp_by_email
from otp import generate_otp, verify_otp, time_limit_input

def main():

    load_dotenv()
    register_or_login = register_login()
    if register_or_login == "register":
        user_input_name = user_name()
        user_input_email = user_email()
        if email_exists:
            sys.exit("This email is already registered!")
        generate = True
        while generate:
            otp = generate_otp()
            message = write_email_message(otp, user_input_email)
            otp_by_email(message)
            user_otp = time_limit_input(180)
            if user_otp:
                if verify_otp(user_otp, otp):
                    print("Verified!")
                    break
                else:
                    print("Incorrect OTP!")
            again = input("Enter 'Resend' to send a new verification code: ")
            if again.lower() == 'resend':
                generate = True
            else:
                sys.exit()
        user_password = user_input_password()
        user_hash_password = hash_password(user_password)
        conn_obj = create_connection_mysql()
        cursor = conn_obj.cursor()
        cursor.execute("USE authenticate_app")
        insert_user_details_db(conn_obj, user_input_name, user_input_email, user_hash_password)
        print("LOGGED IN!")
        closing_connection_mysql(conn_obj)
    else:
        user_input_email = user_email()
        conn_obj = create_connection_mysql()
        cursor = conn_obj.cursor()
        cursor.execute("USE authenticate_app")
        password_hash = retrieve_password_hash_from_email(conn_obj, user_input_email)
        if password_hash:
            user_password = user_input_password()
            if verify_password(user_password, password_hash[0]):
                print("LOGGED IN!") 
            else:
                print("WRONG PASSWORD!")
        else:
            sys.exit("No user was registered with this email.Try Registering! ")

if __name__ == '__main__':
    main()