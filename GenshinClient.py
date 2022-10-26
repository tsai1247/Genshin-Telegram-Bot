from typing import List
import asyncio

import genshin
from genshin import Client
from genshin.client.components.base import *

from TelegramApi import *
from Database.Cookie import *
from ErrorHandler import *

async def redeem_code(update: Update, code: str):
    client = GetClient(update)
    uid = await GetUid(client)
    try:
        await client.redeem_code(code, uid)
    except genshin.RedemptionCooldown:
        await Reply(update, Language.displaywords.str_redeem_cooldown_waiting)
        await asyncio.sleep(3.2)
        await client.redeem_code(code, uid)
        return
    else:
        await Reply(update, f"{Language.displaywords.str_redeem_successful}: {code}")

timer = datetime.now()
async def redeem_code(client: Client, code, attemptTime = 8)-> str: 
    global timer
    await asyncio.sleep(4 - (datetime.now() - timer).seconds)

    uid = await GetUid(client)
    msg = Language.displaywords.str_RedemptionException
    for _attempt in range(attemptTime):
        try:
            await client.redeem_code(code, uid)
            msg = Language.displaywords.str_redeem_successful
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

    timer = datetime.now()
    return msg

async def Redeem_Code(update: Update, codeList: List[str]):
    global timer
    msg = []
    for i in range(len(codeList)):
        code = codeList[i]    
        client = GetClient(update)
        msg.append(await redeem_code(client, code))
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

async def Get_Genshin_Notes(update: Update):
    client = GetClient(update)
    uid = await GetUid(client)
    data = await client.get_genshin_notes(uid)
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
    
    # accounts = await client.get_game_accounts()
    # data = await client.get_genshin_user(accounts[0].uid)
    return client

async def GetUid(client: genshin.Client) -> int:
    accounts = await client.get_game_accounts()
    uid = accounts[0].uid
    return uid