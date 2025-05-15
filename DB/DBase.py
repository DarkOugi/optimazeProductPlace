import psycopg2
import os


class Postgres:
    def __init__(self,host : str,port : str,user:str,password:str,db:str):
        self.host = host if host else os.environ['dbHost']
        self.port = port if port else os.environ['dbPort']
        self.db = db if db else os.environ['dbName']

        self.user = user if user else os.environ['dbUser']
        self.password = password if password else os.environ['dbPassword']
        self.conn = self._connect()
        self.cursor = self.get_cursor()

    def _connect(self):
        try:
            # пытаемся подключиться к базе данных
            return psycopg2.connect(
                dbname=self.db,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except:
            # в случае сбоя подключения будет выведено сообщение в STDOUT
            raise ConnectionError("Can't connect")

    def _cursor(self):

        return self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()