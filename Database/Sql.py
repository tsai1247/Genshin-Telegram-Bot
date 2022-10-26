import sqlite3
from typing import List

class Sql:
    database_path = 'KaTsu.db'

    @staticmethod
    def select(tablename: str, keyfield: List = [], keyvalue: List = [], targetfield: List = ['*'], database_path = database_path) -> List:
        assert len(keyfield) == len(keyvalue)
        if len(keyfield) == 0:
            keyfield = "True"
        else:
            keyfield = ' = ? and '.join(keyfield) + ' = ?'
        targetfield = ', '.join(targetfield)
        
        sql = sqlite3.connect(database_path)
        cur = sql.cursor()
        cur.execute(f"select {targetfield} from {tablename} where {keyfield}", keyvalue)
        data = cur.fetchall()
        cur.close()
        sql.close()
        return data
    
    @staticmethod
    def insert(tablename: str, keyvalue: List = [], database_path = database_path) -> None:
        keyhole = ', '.join(['?'] * len(keyvalue))

        sql = sqlite3.connect(database_path)
        cur = sql.cursor()
        cur.execute(f"insert into {tablename} values({keyhole})", keyvalue)
        sql.commit()
        cur.close()
        sql.close()
    
    @staticmethod
    def update(tablename: str, keyfield: List = [], keyvalue: List = [], targetfield: List = [], targetvalue = [], database_path = database_path, force = False) -> None:
        assert len(keyfield) == len(keyvalue)
        assert len(targetfield) == len(targetvalue)
        assert len(targetfield) > 0, 'the command will always do nothing'
        assert len(keyfield) > 0 or force, 'use "force = True" if you want to update all data in table'

        if len(keyfield) == 0:
            keyfield = "True"
        else:
            keyfield = ' = ? and '.join(keyfield) + ' = ?'
        targetfield = ' = ? and '.join(targetfield) + ' = ?'
        

        sql = sqlite3.connect(database_path)
        cur = sql.cursor()
        cur.execute(f"update {tablename} set {targetfield} where {keyfield}", targetvalue + keyvalue)
        sql.commit()
        cur.close()
        sql.close()
