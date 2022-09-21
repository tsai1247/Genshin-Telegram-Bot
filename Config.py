import sqlite3

class Config:
    def Get(name: str):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select Val from Config where Name = '{0}'".format(name))
        data = cur.fetchone()
        if(data == None or len(data)==0 ):  # init
            initVal = 20
            cur.close()
            cur = sql.cursor()
            cur.execute("insert into Config values('{0}', {1})".format(name, initVal))
            sql.commit()
            data = initVal
        else:
            data = data[0]
        cur.close()
        sql.close()

        return data