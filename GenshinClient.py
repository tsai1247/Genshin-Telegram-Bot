from asyncio import sleep

import genshin
from genshin.client.components.base import *

from TelegramApi import *
from Cookie import *
from ErrorHandler import *

async def redeem_code(update, code):
    client = GetClient(update)
    uid = await GetUid(client)
    try:
        await client.redeem_code(code, uid)
    except genshin.RedemptionCooldown:
        sleep(1.2)
        redeem_code(update, code)
        return
    else:
        await Send(update, "兌換成功")

def GetClient(update: Update):
    cookies = Cookie.Get(GetUserID(update))

    client = genshin.Client(lang='zh-tw')
    client.set_cookies(cookies)
    client.default_game = genshin.Game.GENSHIN
    
    # accounts = await client.get_game_accounts()
    # data = await client.get_genshin_user(accounts[0].uid)
    return client

async def GetUid(client: genshin.Client) -> int:
    accounts = await client.get_game_accounts()
    uid = accounts[0].uid
    return uid