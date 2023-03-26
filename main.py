from operations import *

print('''
1. Sign Up
2. Login
''')

try:
    user = None
    op = int(input('Enter: '))

    if op == 1:
        username = validate_username(input("Enter username: "))
        if get_user(username):
            raise ValueError('Username already exists!')
        
        user = register(
            username,
            password=validate_password(input("Enter password: ")),
            email=validate_email(input("Enter email: ")),
            phone=validate_phone_num(input("Enter phone number: "))
        )
    elif op == 2:
        username = validate_username(input("Enter username: "))
        if not get_user(username):
            raise ValueError('Username doesn\'t exist!')
        
        user = login(
            username,
            password=validate_password(input("Enter password: "))
        )
    else:
        raise ValueError('Enter a valid option.')
except Exception as ex:
    print(ex)

if user:
    print(user)