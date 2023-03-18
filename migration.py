from settings import DATABASES as DB
import pymysql

class Migration:
    # def __init__(self):
    #     self.__conn = self.get_conn

    def get_conn(self, database=None):
        return pymysql.connect(
            host=DB["host"],
            user=DB["user"],
            password=DB["password"], 
            database=database
        )

    def create_database(self):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute(f'''DROP DATABASE IF EXISTS {DB["database"]}''')
        cur.execute(f'''CREATE DATABASE {DB["database"]}''')
        cur.execute(f'''SHOW DATABASES''')
        cur.execute(f'''USE {DB["database"]}''')
        print(f'USING DB {DB["database"]}')
        self.db = f'{DB["database"]}'

        cur.close()
        conn.close()


    def create_tables(self):
        conn = self.get_conn(database=self.db)
        cur = conn.cursor()

        query = """
            CREATE TABLE user (
                id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(128) NOT NULL,
                email VARCHAR(50),
                phone VARCHAR(13)
            )
        """
        
        cur.execute(query)
        cur.close()
        conn.close()
        

db_migration = Migration()

db_migration.create_database()
db_migration.create_tables()