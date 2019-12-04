
import sqlite3

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DB_connection(metaclass=Singleton):
    def __init__(self):
        self.connection = sqlite3.connect('dataBase.db',check_same_thread=False)
        self.cursorObj = self.connection.cursor()
    
    def sql_insert(self, entities, nameTable):
        self.cursorObj.execute('INSERT INTO '+ nameTable +'(name, data) VALUES(?, ?)', entities)
        self.connection.commit()

    def sql_update_rate_null(self, row):
        self.cursorObj.execute('UPDATE rate set fail=null, success=NULL where conversation="'+row+'";')
        self.connection.commit()

    def sql_delete_table(self,name:str):
        self.sql_update_rate_null(name)
        self.cursorObj.execute("DELETE FROM "+name+";")
        self.connection.commit()

    def sql_insert_rate(self,fail,success,name):
        self.cursorObj.execute('UPDATE rate set fail=?, success=? where conversation="'+name+'";', (fail,success))
        self.connection.commit()

    def __del__(self):
        print("close")
        self._db_connection.close()