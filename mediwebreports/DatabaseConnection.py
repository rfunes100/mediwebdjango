import pyodbc

class DatabaseConnection:
    def __init__(self):
        self.conn = pyodbc.connect('Driver={sql server};'
                                   'Server=rdmwipdbuat;'
                                   'Database=mediweb;'
                                   'Trusted_Connection=yes;'
                                   'UID=replicacion;'
                                   'PWD=replicacion;')
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        if params is None:
            return self.cursor.execute(query)
        else:
            return self.cursor.execute(query, params)

    def fetch_all(self):
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()
