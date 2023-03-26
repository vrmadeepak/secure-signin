from operations import *
import traceback



user_id = get_session()
if user_id:
    user = get_user(user_id=user_id)
else:
    user = None
    print(
        'What do you want to do?',
        '1. Sign Up',
        '2. Login',
        sep='\n'
    )

if not user:    
    op = int(input('> '))

    if op == 1:
        username = validate_username(input("Enter username: "))
        if get_user(username=username):
            raise ValueError('Username already exists!')
        
        user = register(
            username,
            password=validate_password(input("Enter password: ")),
            email=validate_email(input("Enter email: ")),
            phone=validate_phone_num(input("Enter phone number: "))
        )
    elif op == 2:
        username = validate_username(input("Enter username: "))
        if not get_user(username=username):
            raise ValueError('Username doesn\'t exist!')
        
        user = login(
            username,
            password=validate_password(input("Enter password: "))
        )
    else:
        raise ValueError('Enter a valid option.')
# except Exception as ex:
#     # traceback.print_exc()
#     print(ex)

if user:
    print(user)
    print(
        'What do you want to do?', 
        '1. Logout',
        '2. Edit Profile',
        sep='\n'
    )
    op = int(input('> '))
    if op == 1:
        delete_session(user_id)
        del user
    elif op == 2:
        print('')