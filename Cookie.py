import sqlite3
import json
class Cookie:
    @staticmethod
    def Get(ID: str):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select * from Cookie where userID = '{0}'".format(ID))
        data = cur.fetchone()
        if(data == None or len(data)==0 ):
            data = None
        else:
            data = {'ltuid': data[1], 'ltoken': data[2], 'cookie_token': data[3], 'account_id': data[4]}
        cur.close()
        sql.close()

        return data

    @staticmethod
    def Set(ID: str, cookie):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select userID from Cookie where userID = '{0}'".format(ID))
        data = cur.fetchone()
        ltuid = cookie.split('ltuid=')[1].split(';')[0]
        ltoken = cookie.split('ltoken=')[1].split(';')[0]
        cookie_token = cookie.split('cookie_token=')[1].split(';')[0]
        account_id = cookie.split('account_id=')[1].split(';')[0]
        if(data == None or len(data)==0 ):  # insert
            cur.close()
            cur = sql.cursor()
            cur.execute("insert into Cookie values('{0}', '{1}', '{2}', '{3}', '{4}')".format(ID, ltuid, ltoken, cookie_token, account_id))
            sql.commit()
        else:                               # update
            cur.close()
            cur = sql.cursor()
            cur.execute("update Cookie set ltuid = '{1}', ltoken = '{2}', cookie_token = '{3}', account_id = '{4}' where userID = '{0}'".format(ID, ltuid, ltoken, cookie_token, account_id))
            sql.commit()
        cur.close()
        sql.close()
