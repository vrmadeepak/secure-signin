from operations import *

def register():
    username = validate_username(input("Enter username: "))
    password = validate_password(input("Enter password: "))
    email = validate_email(input("Enter email: "))
    phone = validate_phone_num(input("Enter phone number: "))

    if not (phone or email):
        raise ValueError('Phone Number or Email is required')
    
    add_user(username, password, email, phone)
    # conn = get_conn()

def login():
    username = validate_username(input("Enter username: "))
    password = validate_password(input("Enter password: "))

    validate_user(username, password)