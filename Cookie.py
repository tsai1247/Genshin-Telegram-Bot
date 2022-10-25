import sqlite3
import genshin

class Cookie:
    @staticmethod
    def Get(userID: int):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select * from Cookie where userID = ?", [userID])
        data = cur.fetchone()
        if(data == None):
            raise genshin.errors.InvalidCookies
        else:
            data = {'ltuid': data[1], 'ltoken': data[2], 'cookie_token': data[3], 'account_id': data[4]}
        cur.close()
        sql.close()

        return data

    @staticmethod
    def Set(ID: int, cookie: str):
        ltuid = cookie.split('ltuid=')[1].split(';')[0]
        ltoken = cookie.split('ltoken=')[1].split(';')[0]
        cookie_token = cookie.split('cookie_token=')[1].split(';')[0]
        account_id = cookie.split('account_id=')[1].split(';')[0]
        
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select userID from Cookie where userID = ?", [ID])
        data = cur.fetchone()
        if(data == None):   # insert
            cur.close()
            cur = sql.cursor()
            cur.execute("insert into Cookie values(?, ?, ?, ?, ?)", [ID, ltuid, ltoken, cookie_token, account_id])
            sql.commit()
        else:               # update
            cur.close()
            cur = sql.cursor()
            cur.execute("update Cookie set ltuid = ?, ltoken = ?, cookie_token = ?, account_id = ? \
                         where userID = ?", [ltuid, ltoken, cookie_token, account_id, ID])
            sql.commit()
        cur.close()
        sql.close()
