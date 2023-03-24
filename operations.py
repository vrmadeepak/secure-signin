from settings import DATABASES as DB
import pymysql
import hashlib

def get_conn() -> object:
    """
    Get sql conn object
    """
    return pymysql.connect(
            host=DB["host"],
            user=DB["user"],
            password=DB["password"], 
            database=DB["database"]
        )

def get_user(username: str) -> tuple:
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f'''
            SELECT username from users
            WHERE username = '{username}'
            '''
        )
        res = cur.fetchall()
        cur.close()
        return res
    
def add_user(username: str, password: str, email: str, phone: str):
    with get_conn() as conn:
        cur = conn.cursor()

        if not email:
            cur.execute(
                f'''
                INSERT INTO users (username, password, phone)
                VALUES ('{username}', '{password}', '{phone}')
                '''
            )
        elif not phone:
            cur.execute(
                f'''
                INSERT INTO users (username, password, email)
                VALUES ('{username}', '{password}', '{email}')
                '''
            )
        else:
            cur.execute(
                f'''
                INSERT INTO users (username, password, email, phone)
                VALUES ('{username}', '{password}', '{email}', '{phone}')
                '''
            )
        cur.close()
        conn.commit()

def validate_user(username, password):
    with get_conn() as conn:
        cur = conn.cursor()

        cur.execute(
            f'''
            SELECT * FROM 
            '''
        )

def validate_phone_num(phone_num: str) -> str:
    """
    This Function validates the phone number for only Indian numbers.
    """
    phone_num = phone_num.replace(" ", "").replace("-", "").replace("+", "")
    if not phone_num:
        return phone_num
    elif phone_num.isdigit():
        if len(phone_num) == 12 and phone_num.startswith('91'):
            return '+' + phone_num
        elif len(phone_num) == 10:
            return '+91' + phone_num
    
    raise ValueError('Phone number is not valid.')


def validate_email(email: str) -> str:
    """
    Validate an email address
    """
    email = email.strip()
    if not email:
        return email
    elif email and email.count('@') == 1 and email.count('.') >= 1:
    #     email = email.split('@')
        return email
    
    raise ValueError('Email address is not valid.')

def validate_password(password: str) -> str:
    """
    Validate User Password
    """
    password = password.strip()
    if password:
        password = hashlib.sha512(password.encode())
        return password.hexdigest()
    raise ValueError('Enter a Valid Password!')
    
def validate_username(username: str) -> str:
    """
    Validate Username
    """
    username = username.strip()
    if username:
        if get_user(username):
            raise ValueError('User already Exists!')
        return username
    raise ValueError('Username cannot be empty!')
