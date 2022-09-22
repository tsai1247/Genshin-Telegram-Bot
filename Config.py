import sqlite3

class Config:
    def Get(name: str):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select Val from Config where Name = ?", [name])
        data = cur.fetchone()
        if(data == None):  # init
            initVal = 20
            cur.close()
            cur = sql.cursor()
            cur.execute("insert into Config values(?, ?)", [name, initVal])
            sql.commit()
            data = initVal
        else:
            data = data[0]
        cur.close()
        sql.close()

        return data