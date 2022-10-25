from asyncio import sleep
import asyncio

import genshin
from genshin.client.components.base import *

from TelegramApi import *
from Cookie import *
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