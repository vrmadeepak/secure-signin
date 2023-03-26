from settings import DATABASES as DB
import pymysql
import hashlib
from datetime import datetime
import uuid

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

def get_user(user_id: int = None, username: str = None) -> tuple:
    with get_conn() as conn:
        cur = conn.cursor()
        if user_id:
            cond = f"id = {user_id}"
        elif username:
            cond = f"username = '{username}'"
        cur.execute(
            f'''
            SELECT id, username, email, phone FROM users
            WHERE {cond}
            '''
        )
        res = cur.fetchall()
        cur.close()
        if res:
            return res[0]

def create_session(user_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f'''
            INSERT INTO sessions (data, user_id, created_at, updated_at)
            VALUES ('{uuid.uuid4()}', {user_id}, '{datetime.now()}', '{datetime.now()}')
            '''
        )
        conn.commit()
        cur.close()

def update_session(user_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f'''
            UPDATE sessions 
            SET data='{uuid.uuid4()}', updated_at='{datetime.now()}'
            WHERE user_id={user_id}
            '''
        )
        cur.close()

def get_session():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f'''
            SELECT user_id from sessions
            '''
        )

        res = cur.fetchall()
        cur.close()
        if res:
            return res[0][0]

def delete_session(user_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f'''
            DELETE FROM sessions
            WHERE user_id = {user_id}
            '''
        )
        cur.close()
        conn.commit()

def validate_user(username, password):
    # TODO: why are we using validate_user...
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
    raise ValueError('Password cannot be empty!')
    
def validate_username(username: str) -> str:
    """
    Validate Username
    """
    username = username.strip()
    if username:
        return username
    raise ValueError('Username cannot be empty!')

def register(username, password, email, phone):
    if not (phone or email):
        raise ValueError('Phone Number or Email is required')
    
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
        conn.commit()
        cur.close()
        
        res = get_user(username=username)
        if res:
            create_session(res[0])
            return res
    
def login(username, password):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f'''
            SELECT id, username, email, phone FROM users
            WHERE username='{username}' AND password='{password}'
            '''
        )
        res = cur.fetchall()
        cur.close()
        if res:
            create_session(res[0][0])
            return res[0]
    raise ValueError('Incorrect Password!')

def logout(user_id):
    with get_conn() as conn:
        cur = conn.cursor()
        
# TODO: SESSION FLOW - WHEN DID USER LOGIN, LAST_LOGIN ETC...