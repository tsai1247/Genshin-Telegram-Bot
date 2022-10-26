from .Sql import Sql

class Config:
    tablename = 'Config'

    @staticmethod
    def Get(name: str):
        data = Sql.select(Config.tablename, keyfield=['Name'], keyvalue=[name], targetfield=['Val'])

        if len(data) == 0:  # init
            initVal = 20
            Sql.insert(Config.tablename, keyvalue=[name, initVal])
            data = initVal
        else:
            data = data[0][0]

        return data