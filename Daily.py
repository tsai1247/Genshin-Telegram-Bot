import asyncio
from datetime import datetime
import logging
import sqlite3
import genshin

from GenshinClient import GetClient
from Language import Language
from TelegramApi import Send

class Daily:
    @staticmethod
    def Get(userID: int):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select * from Daily where userID = ?", [userID])
        data = cur.fetchone()
        if(data == None):
            data = {'autoDaily': 0}
        else:
            data = {'autoDaily': data[1]}
        cur.close()
        sql.close()

        return data

    @staticmethod
    def GetAll(autoDaily = 1):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select * from Daily where autoDaily = ?", [autoDaily])
        data = cur.fetchall()
        cur.close()
        sql.close()

        data = [i[0] for i in data]
        return data

    @staticmethod
    def Set(ID: int, autoDaily: int):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select userID from Daily where userID = ?", [ID])
        data = cur.fetchone()
        if(data == None):   # insert
            cur.close()
            cur = sql.cursor()
            cur.execute("insert into Daily values(?, ?)", [ID, autoDaily])
            sql.commit()
        else:               # update
            cur.close()
            cur = sql.cursor()
            cur.execute("update Daily set autoDaily = ? \
                         where userID = ?", [autoDaily, ID])
            sql.commit()
        cur.close()
        sql.close()

    @staticmethod
    async def AutoClaim(hour=4, minute=1, second = 0):
        logging.info('auto claim thread start')
        while True:
            now = datetime.now()
            tomorrow = datetime.now()
            tomorrow = tomorrow.replace(day = tomorrow.day + 1, hour=hour, minute=minute, second=second)

            wait_for = (tomorrow - now).seconds

            logging.info(f'Auto claim mission finished.  Sleep for {wait_for} seconds')
            await asyncio.sleep(wait_for)
            
            userIDList = Daily.GetAll()
            for userID in userIDList:
                try:
                    client = GetClient(userID)
                    reward = await client.claim_daily_reward(game=genshin.Game.GENSHIN)
                    await Send(userID, f'{Language.displaywords.str_daily_successful} {reward.amount}x {reward.name}！')
                except genshin.errors.InvalidCookies as e:
                    await Send(userID, Language.displaywords.str_InvalidCookies_when_Daiily)
                    logging.info(f"[例外]: [retcode]{e.retcode} [原始內容]{e.original} [錯誤訊息]{e.msg}")
                except genshin.errors.AlreadyClaimed as e:
                    await Send(userID, Language.displaywords.str_AlreadyClaimed)



