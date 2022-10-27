import asyncio
from datetime import datetime
import logging
import genshin
from Database.Sql import Sql

from GenshinClient import GetClient
from Language import Language
from TelegramApi import Send

class Daily:
    tablename = 'Daily'

    @staticmethod
    def Get(userID: int):
        data = Sql.select(Daily.tablename, keyfield=['userID'], keyvalue=[userID])

        if len(data) == 0:
            data = {'autoDaily': 0}
        else:
            data = {'autoDaily': data[0][1]}

        return data

    @staticmethod
    def GetAll(autoDaily = 1):
        data = Sql.select(Daily.tablename, keyfield=['autoDaily'], keyvalue=[autoDaily])

        data = [i[0] for i in data]
        return data

    @staticmethod
    def Set(userID: int, autoDaily: int):
        data = Sql.select(Daily.tablename, keyfield=['userID'], keyvalue=[userID])

        if len(data) == 0:   # insert
            Sql.insert(Daily.tablename, keyvalue=[userID, autoDaily])
        else:               # update
            Sql.update(Daily.tablename, keyfield=['userID'], keyvalue=[userID], targetfield=['autoDaily'], targetvalue=[autoDaily])

    @staticmethod
    async def AutoClaim(hour=4, minute=1, second = 0):
        logging.info('auto claim thread start')
        while True:
            now = datetime.now()
            tomorrow = datetime.now()
            tomorrow = tomorrow.replace(day = tomorrow.day + 1, hour=hour, minute=minute, second=second)

            wait_for = (tomorrow - now).seconds
            str_wait_for = f'{wait_for//60//60} hr(s), {wait_for//60%60} min(s), {wait_for%60} sec(s)' 
            logging.info(f'Auto claim mission finished.  Sleep for {str_wait_for}')
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
                except genshin.errors.AlreadyClaimed:
                    await Send(userID, Language.displaywords.str_AlreadyClaimed)



