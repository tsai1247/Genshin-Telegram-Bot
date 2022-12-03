import asyncio
from datetime import datetime, timedelta
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
        def getNextDay(hour = hour, minute = minute, second = second):
            ret = datetime.now() + timedelta(hours=23, minutes=59, seconds=59)
            ret = ret.replace(hour=hour, minute=minute, second=second)
            return ret

        def getWaitSeconds():
            A_DAY = 60*60*24
            now = datetime.now()
            ori = datetime.now().replace(hour=hour, minute=minute, second=second)
            return A_DAY - (now - ori).seconds

        logging.info('auto claim thread start')
        while True:
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

            wait_for = getWaitSeconds()
            str_wait_for = f'{wait_for//60//60} hr(s), {wait_for//60%60} min(s), {wait_for%60} sec(s)' 
            logging.info(f'Auto claim mission finished.  Sleep for {str_wait_for}')
            await asyncio.sleep(wait_for)
            


