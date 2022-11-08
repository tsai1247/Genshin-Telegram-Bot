from enum import Enum
import sqlite3
from typing import List

class Sql:
    class Type(Enum):
        TEXT = 'TEXT'
        INTEGER = 'INTEGER'
        INTEGERUNIQUE = 'INTEGER UNIQUE'

    database_path = 'KaTsu.db'
    @staticmethod
    def create(tablename: str, fieldname: List = [], fieldtype: List[Type] = [], primarykey: List = [], database_path = database_path):
        assert len(fieldname) == len(fieldtype), 'create error'
        field = []
        for i in range(len(fieldname)):
            field.append(f'"{fieldname[i]}" {fieldtype[i].value}')
        
        field = ', \n'.join(field)
        if len(primarykey) > 0:
            primarykey = f', PRIMARY KEY("{", ".join(primarykey)}")'
        else:
            primarykey = ''
        
        command = f'CREATE TABLE "{tablename}" (\n'\
                + field + '\n' \
                + primarykey + '\n' \
                + ')'

        Sql.execute(command, database_path=database_path)

    @staticmethod
    def select(tablename: str, keyfield: List = [], keyvalue: List = [], targetfield: List = ['*'], database_path = database_path) -> List:
        assert len(keyfield) == len(keyvalue)
        if len(keyfield) == 0:
            keyfield = "True"
        else:
            keyfield = ' = ? and '.join(keyfield) + ' = ?'
        targetfield = ', '.join(targetfield)
        
        data = Sql.execute(f"select {targetfield} from {tablename} where {keyfield}", keyvalue, database_path)
        return data
    
    @staticmethod
    def insert(tablename: str, keyvalue: List = [], database_path = database_path) -> None:
        keyhole = ', '.join(['?'] * len(keyvalue))

        Sql.execute(f"insert into {tablename} values({keyhole})", keyvalue, database_path)
    
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
        targetfield = ' = ?, '.join(targetfield) + ' = ?'
        
        Sql.execute(f"update {tablename} set {targetfield} where {keyfield}", targetvalue + keyvalue, database_path)

    @staticmethod
    def execute(command: str, param: List = [], database_path = database_path):
        sql = sqlite3.connect(database_path)
        cur = sql.cursor()
        cur.execute(command, param)
        data = cur.fetchall()
        sql.commit()
        cur.close()
        sql.close()
        return data

    @staticmethod
    def exists(tablename: str, database_path = database_path):
        command = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tablename}'"
        data = Sql.execute(command, database_path=database_path)
        return  len(data) > 0