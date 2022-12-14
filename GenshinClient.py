from typing import Sequence
import asyncio

import genshin
from genshin import Client
from genshin.client.components.base import *
from genshin.models import GenshinAccount

from TelegramApi import *
from Database.Cookie import *
from ErrorHandler import *

timer = datetime.now()
async def redeem_code(client: Client, code, attemptTime = 8)-> str: 
    global timer
    cooldowntime = 5
    await asyncio.sleep(cooldowntime - (datetime.now() - timer).seconds)

    uidList = await GetUid(client)

    msgList = []
    for uid in uidList:
        msg = Language.displaywords.str_RedemptionException
        for _attempt in range(attemptTime):
            try:
                await client.redeem_code(code, uid)
                msg = Language.displaywords.str_redeem_successful
                break
            except genshin.RedemptionCooldown:
                await asyncio.sleep(1)
                continue
            except genshin.RedemptionClaimed:
                msg = Language.displaywords.str_RedemptionClaimed
                break
            except genshin.RedemptionInvalid:
                msg = Language.displaywords.str_RedemptionInvalid
                break
            except genshin.RedemptionException:
                msg = Language.displaywords.str_RedemptionException
                break
        msgList.append(f'  UID {uid}: {msg}')

    timer = datetime.now()
    return '\n'.join(msgList)

async def Redeem_Code(update: Update, code: str):
    global timer
    client = GetClient(update)
    msg = await redeem_code(client, code)
    return msg

async def Claim_Daily_Reward(update: Update):
    try:
        client = GetClient(update)
        reward = await client.claim_daily_reward(game=genshin.Game.GENSHIN)
        msg = f'{Language.displaywords.str_daily_successful} {reward.amount}x {reward.name}！'
    except genshin.errors.InvalidCookies:
        msg = f'{Language.displaywords.str_InvalidCookies}'
    except genshin.errors.AlreadyClaimed:
        msg = f'{Language.displaywords.str_AlreadyClaimed}'

    return msg

async def Get_Genshin_Notes(update: Update, server: str):
    client = GetClient(update)
    uid = await GetUid(client, server)
    data: Notes = await client.get_genshin_notes(uid)
    msg = [
        Language.displaywords.GetResinMsg(data),
        Language.displaywords.GetRealmCurrencyMsg(data),
        Language.displaywords.GetCommissionsMsg(data),
        Language.displaywords.GetResin_DiscountsMsg(data),
        Language.displaywords.GetTransformerMsg(data),
        Language.displaywords.GetExpeditionsMsg(data)
    ]

    return msg

def GetClient(update: Union[Update, int]):
    if type(update) is Update:
        userID = GetUserID(update)
    else:
        userID = update
    cookies = Cookie.Get(userID)
    client = genshin.Client(lang='en-us')

    client.set_cookies(cookies)
    client.default_game = genshin.Game.GENSHIN
    
    return client

async def GetUid(client: genshin.Client, server: Union[str, None] = None) -> int:
    if server == None:
        accounts = await client.genshin_accounts()
        uidList = [account.uid for account in accounts]
    else:
        accounts = list(filter(lambda account: account.server == server, await client.genshin_accounts()))
        assert len(accounts) == 1
        uidList = accounts[0].uid        
    
    return uidList

async def GetAccounts(client: genshin.Client):
    accounts = await client.genshin_accounts()
    return accounts

async def GetServer(client: genshin.Client):
    accounts: Sequence[GenshinAccount] = await GetAccounts()
    serverList = [account.server for account in accounts]
    return serverList

