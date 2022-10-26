import genshin
from .Sql import Sql

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
    def Set(userID: int, cookie: str):
        try:
            ltuid = cookie.split('ltuid=')[1].split(';')[0]
            ltoken = cookie.split('ltoken=')[1].split(';')[0]
            cookie_token = cookie.split('cookie_token=')[1].split(';')[0]
            account_id = cookie.split('account_id=')[1].split(';')[0]
            

            data = Sql.select(Cookie.tablename, keyfield=['userID'], keyvalue=[userID])
            if len(data) == 0:   # insert
                Sql.insert(Cookie.tablename, keyvalue=[userID, ltuid, ltoken, cookie_token, account_id])
            else:               # update
                Sql.update(Cookie.tablename, keyfield=['userID'], keyvalue=[userID], targetfield=["ltuid", "ltoken", "cookie_token", "account_id"], targetvalue=[ltuid, ltoken, cookie_token, account_id])
            msg = Language.displaywords.str_cookie_successful
        except:
            msg = Language.displaywords.str_cookie_fail
            
        return msg
