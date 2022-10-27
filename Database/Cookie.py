from typing import Dict
import genshin
from .Sql import Sql
from http.cookies import SimpleCookie
from Language import Language

class Cookie:
    tablename = 'Cookie'

    @staticmethod
    def Get(userID: int):
        data = Sql.select(Cookie.tablename, keyfield=['userID'], keyvalue=[userID])
        if len(data) == 0:
            raise genshin.errors.InvalidCookies
        else:
            data = data[0]
            data = {'ltuid': data[1], 'ltoken': data[2], 'cookie_token': data[3], 'account_id': data[4]}

        return data

    @staticmethod
    def Dumps(text: str): # "a=?, b=?, c=?"
        cookie = SimpleCookie()
        cookie.load(text)
        return {k: v.value for k, v in cookie.items()}

    @staticmethod
    def Set(userID: int, cookie: Dict):
        try:
            ltuid = cookie['ltuid']
            ltoken = cookie['ltoken']
            cookie_token = cookie['cookie_token']
            account_id = cookie['account_id']

            data = Sql.select(Cookie.tablename, keyfield=['userID'], keyvalue=[userID])
            if len(data) == 0:   # insert
                Sql.insert(Cookie.tablename, keyvalue=[userID, ltuid, ltoken, cookie_token, account_id])
            else:               # update
                Sql.update(Cookie.tablename, keyfield=['userID'], keyvalue=[userID], targetfield=["ltuid", "ltoken", "cookie_token", "account_id"], targetvalue=[ltuid, ltoken, cookie_token, account_id])
            msg = Language.displaywords.str_cookie_successful
        except:
            msg = Language.displaywords.str_cookie_fail
            
        return msg
