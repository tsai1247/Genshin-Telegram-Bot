from Security import isDos
from Variable.String import *
from TelegramApi import *
from Cookie import *
from GenshinClient import *

import genshin

class UserStatus:
    statusList = {}

    # enum list
    SetCookie = 1
    RedeemCode = 2
    
    def GetKey(key: Union[Update, str]) -> int:
        if type(key) is Update:
            key = GetUserID(key)
        return key

    @staticmethod
    def set(key: Union[Update, int], value: int) -> None:
        key = UserStatus.GetKey(key)
        UserStatus.statusList[key] = value

    @staticmethod
    def get(key) -> int:
        key = UserStatus.GetKey(key)
        if key in UserStatus.statusList:
            return UserStatus.statusList[key]
        else:
            return None

    @staticmethod
    def delete(key) -> None:
        key = UserStatus.GetKey(key)
        if key in UserStatus.statusList:
            del UserStatus.statusList[key]

async def startbot(update: Update, bot):
    if(isDos(update)): return
    await Send(update, str_welcome)

async def help(update: Update, bot):
    if(isDos(update)): return
    await Send(update, str_help)

async def setcookie(update: Update, bot):
    if(isDos(update)): return
    await Send(update, "請輸入你的cookie：", forceReply = True)
    await Send(update, str_cookie_tutorial)
    await Send(update, str_cookie_javascript_command)
    UserStatus.set(update, UserStatus.SetCookie)

async def daily(update: Update, bot):
    if(isDos(update)): return
    client = GetClient(update)
    reward = await client.claim_daily_reward(game=genshin.Game.GENSHIN)
    await Send(update, f'今日簽到成功，獲得 {reward.amount}x {reward.name}！')

async def note(update: Update, bot):
    if(isDos(update)): return

    client = GetClient(update)
    accounts = await client.get_game_accounts()
    uid = accounts[0].uid
    data = await client.get_genshin_notes(uid)
    
    await Send(update, [
        GetResinMsg(data),
        GetRealmCurrencyMsg(data),
        GetCommissionsMsg(data),
        GetResin_DiscountsMsg(data),
        GetTransformerMsg(data),
        GetExpeditionsMsg(data)
    ])  

async def gift(update: Update, bot):
    await Send(update, "請輸入兌換碼", forceReply = True)
    UserStatus.set(update, UserStatus.RedeemCode)

async def hi(update: Update, bot):
    try:
        await Send(update, f"hi, {update.message.from_user.name}")
    except:
        await Send(update, f"hi, {update.message.from_user.first_name}")
    
async def notice(update: Update, bot):
    if(isDos(update)): return
    NotImplemented()

async def setaccount(update: Update, bot):
    if(isDos(update)): return
    NotImplemented()

async def lang(update: Update, bot):
    if(isDos(update)): return
    NotImplemented()

async def getText(update: Update, bot):
    if(isDos(update)): return
    if UserStatus.get(update) == UserStatus.SetCookie:
        cookie = update.message.text
        Cookie.Set(GetUserID(update), cookie)
        await Send(update, "cookie已更新")
        UserStatus.delete(update)
        
    elif UserStatus.get(update) == UserStatus.RedeemCode:
        code = update.message.text
        await redeem_code(update, code)
        UserStatus.delete(update)
        
async def callback(update: Update, bot):
    if(isDos(update)): return
    # text, userID = update.callback_query.data.split(" ")
    NotImplemented()