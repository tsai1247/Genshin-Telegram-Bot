from Language import Language
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
    Language = 3
    
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
    appendlog(update)
    await Reply(update, Language.displaywords.str_welcome)
    

async def help(update: Update, bot):
    if(isDos(update)): return
    appendlog(update)
    await Reply(update, Language.displaywords.str_help)
    

async def setcookie(update: Update, bot):
    if(isDos(update)): return
    appendlog(update)

    await Reply(update, Language.displaywords.str_enter_cookie, forceReply = True)
    await Reply(update, Language.displaywords.str_cookie_tutorial)
    await Reply(update, Language.displaywords.str_cookie_javascript_command)
    UserStatus.set(update, UserStatus.SetCookie)
    
async def daily(update: Update, bot):
    if(isDos(update)): return
    appendlog(update)

    client = GetClient(update)
    reward = await client.claim_daily_reward(game=genshin.Game.GENSHIN)
    await Reply(update, f'{Language.displaywords.str_daily_successful} {reward.amount}x {reward.name}！')
    

async def note(update: Update, bot):
    if(isDos(update)): return
    appendlog(update)

    client = GetClient(update)
    accounts = await client.get_game_accounts()
    uid = accounts[0].uid
    data = await client.get_genshin_notes(uid)
    
    await Reply(update, [
        Language.displaywords.GetResinMsg(data),
        Language.displaywords.GetRealmCurrencyMsg(data),
        Language.displaywords.GetCommissionsMsg(data),
        Language.displaywords.GetResin_DiscountsMsg(data),
        Language.displaywords.GetTransformerMsg(data),
        Language.displaywords.GetExpeditionsMsg(data)
    ])  
    

async def gift(update: Update, bot):    
    if(isDos(update)): return
    appendlog(update)
    await Reply(update, {Language.displaywords.str_enter_redeem_code}, forceReply = True)
    UserStatus.set(update, UserStatus.RedeemCode)
    

async def hi(update: Update, bot):
    appendlog(update)
    try:
        await Reply(update, f"hi, {update.message.from_user.name}")
    except:
        await Reply(update, f"hi, {update.message.from_user.first_name}")
    

async def notice(update: Update, bot):
    if(isDos(update)): return
    NotImplemented()

async def setaccount(update: Update, bot):
    if(isDos(update)): return
    NotImplemented()

async def lang(update: Update, bot):
    if(isDos(update)): return
    appendlog(update)

    userID = GetUserID(update)
    await ReplyButton(update, title = f'{Language.displaywords.str_current_lang}{Language.Get(userID)}', 
        buttonText = [['中文', 'English']], 
        replyText = [[f'{UserStatus.Language}\\{userID}\\zhTW', f'{UserStatus.Language}\\{userID}\\en']]
    )
    

async def getText(update: Update, bot):
    if(isDos(update)): return
    appendlog(update)

    if UserStatus.get(update) == UserStatus.SetCookie:
        appendlog(update, 'set cookie')
        cookie = update.message.text
        Cookie.Set(GetUserID(update), cookie)
        await Reply(update, Language.displaywords.str_cookie_successful)
        UserStatus.delete(update)
        

    elif UserStatus.get(update) == UserStatus.RedeemCode:
        appendlog(update, 'redeemCode')
        code = update.message.text
        await redeem_code(update, code)
        UserStatus.delete(update)
        
        
async def callback(update: Update, bot):
    status, userID, text = update.callback_query.data.split("\\")
    appendlog(int(userID), 'call back (button clicked)')
    if int(status) == UserStatus.Language:
        appendlog(int(userID), 'switch language')

        Language.Set(int(userID), text)
        await Send(int(userID), f"{Language.displaywords.str_switch_lang_success}{text}")
        