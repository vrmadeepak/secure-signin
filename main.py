from settings import DATABASES as DB
import hashlib
import pymysql

def validate_user_details(detail, context):
    detail = detail if context=="password" else detail.strip()
    # if detail.count(" "):
    #     print(det)
    if context=="username":
        return detail
    elif context=="email":
        return detail
    elif context=="phone":
        phone = detail.replace(" ", "").replace("-", "").replace("+", "")
        if phone.isdigit():
            if len(phone)==12:
                return "+" + phone
            elif len(phone)==10:
                return "+91" + phone
        raise ValueError("Phone Number not valid")
    
    elif context=="password":
        password = hashlib.sha512(detail.encode())
        return password.hexdigest()
    
def get_conn():
    return pymysql.connect(
            host=DB["host"],
            user=DB["user"],
            password=DB["password"], 
            database=DB["database"]
        )

def register():
    username = validate_user_details(input("Enter username: "), "username")
    email = validate_user_details(input("Enter email: "), "email")
    password = validate_user_details(input("Enter password: "), "password")
    phone = validate_user_details(input("Enter phone number: "), "phone")

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            f'''
            INSERT INTO user (username, email, phone, password)
            VALUES '{username}', '{email}', '{phone}', '{password}'
            '''
        )
        cur.close()
        conn.commit()
    # conn = get_conn()




register()