from .Sql import Sql

class Config:
    tablename = 'Config'

    @staticmethod
    def Get(name: str):
        data = Sql.select(Config.tablename, keyfield=['Name'], keyvalue=[name], targetfield=['Val'])

        if len(data) == 0:
            data = {'Val': None}
        else:
            data = {'Val': data[0][0]}

        return data

    @staticmethod
    def Set(Name: str, Val: int):
        data = Sql.select(Config.tablename, keyfield=['Name'], keyvalue=[Name])
        if len(data) == 0:   # insert
            Sql.insert(Config.tablename, keyvalue=[Name, Val])
        else:               # update
            Sql.update(Config.tablename, keyfield=['Name'], keyvalue=[Name], targetfield=["Val"], targetvalue=[Val])
