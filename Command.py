from asyncio import sleep
from collections import UserDict
from datetime import datetime, timedelta, timezone
import types
from typing import Sequence
from dosdefence import isDos, getID
from os import getenv
from function import *
import sqlite3
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import random
from Cookie import *
import genshin
from genshin.client import cache as client_cache
from genshin.models import hoyolab as hoyolab_models
from genshin.client.components.base import *
from genshin.models.genshin import chronicle as models

class UserStatus:
    statusList = {}
    # enum list
    SetCookie = 1
    RedeemCode = 2

    @staticmethod
    def set(key, value):
        if type(key) is not str:
            key = getID(key)
        UserStatus.statusList[key] = value

    @staticmethod
    def get(key):
        if type(key) is not str:
            key = getID(key)
        if key in UserStatus.statusList:
            return UserStatus.statusList[key]
        else:
            return None

    @staticmethod
    def delete(key):
        if type(key) is not str:
            key = getID(key)
        if key in UserStatus.statusList:
            del UserStatus.statusList[key]

def isAttack(text):
    if '*' in text or '?' in text or '%' in text or '+' in text or '_' in text:
        return True
    if "\"" in text or '\'' in text:
        return True
    return False

async def startbot(update, bot):
    if(isDos(update)): return
    await Send(update, "嗨")
    await Send(update, "我可以幫你的原神每日簽到以及提醒資源的狀況")
    await Send(update, "使用 /help 來取得更多資訊")

async def help(update, bot):
    if(isDos(update)): return
    await Send(update, "你可能會想要：")
    await Send(update, "0. 第一次使用此bot時，使用 /cookie 設定你的 cookie。\n" + \
                 "  cookie 可以讓 bot 協助你取得 hoyolab 上的資訊\n" + \
                 "  (請放心，持有 cookie並無法修改你的任何遊戲進度)")
    await Send(update, "1. 使用 /daily 開啟或關閉原神每日簽到，協助你確實領到每日簽到獎勵")
    await Send(update, "2. 使用 /notice 在樹脂將滿時、洞天寶錢將滿時、探索完成時提醒你")
    await Send(update, "3. 使用 /info 即時確認樹脂、洞天寶錢、探索狀態等數值")
    await Send(update, "4. 使用 /account 在你的 cookie 因為不明原因頻繁更換時，你可以直接提供 hoyolab 的帳號密碼給 bot ，讓 bot 來主動更新 cookie。\n" + \
                 "(請注意：若你不信任此 bot 的提供者，請勿使用此指令來交付帳號密碼。你當然可以自行在 hoyolab 上修改帳號密碼使此功能失效。)")



async def callback(update, bot):
    if(isDos(update)): return
    text, userID = update.callback_query.data.split(" ")
    await Send(update, "callback")

async def setcookie(update, bot):
    if(isDos(update)): return
    await Send(update, "請輸入你的cookie：", forceReply = True)
    await Send(update, "步驟一： 使用瀏覽器進入 https://www.hoyolab.com/ ，並且登入\n" + \
        "步驟二： 將網址欄清空，輸入java後貼上下方文字，確認文字開頭為「javascript:」，並沒有多餘的引號或空格後，按下Enter\")\n" + \
        "步驟三： 將網頁顯示的文字全選，複製後貼到此聊天室\n" + \
        "更詳細的內容請參閱 https://genshin.xiaokuai.tk/cookie幫助/")

    await Send(update, "script:d=document.cookie; c=d.includes('account_id') || alert('過期或無效的Cookie,請先登出帳號再重新登入!'); c && document.write(d)")
    UserStatus.set(getID(update), UserStatus.SetCookie)

async def getText(update, bot):
    if(isDos(update)): return
    if UserStatus.get(update) == UserStatus.SetCookie:
        cookie = update.message.text
        Cookie.Set(getID(update), cookie)
        await Send(update, "cookie已更新")
        UserStatus.delete(update)
    elif UserStatus.get(update) == UserStatus.RedeemCode:
        code = update.message.text
        await redeem_code(update, code)
        UserStatus.delete(update)

async def redeem_code(update, code):
    client = getClient(update)

    accounts = await client.get_game_accounts()
    uid = accounts[0].uid
    try:
        await client.redeem_code(code, uid)
    except genshin.errors.InvalidCookies:
        msg = 'Cookie已失效，請從Hoyolab重新取得新Cookie'
    except genshin.RedemptionClaimed:
        msg = '兌換碼已被使用'
    except genshin.RedemptionCooldown:
        sleep(1.2)
        redeem_code(update, code)
        return
    except genshin.RedemptionInvalid:
        msg = '無效的兌換碼'
    except genshin.RedemptionException as e:
        msg =  f'兌換失敗：[retcode]{e.retcode} [內容]{e.original}'
    else:
        msg = "兌換成功"
    await Send(update, msg)

async def daily(update, bot):
    if(isDos(update)): return
    client = getClient(update)
    try:
        reward = await client.claim_daily_reward(game=genshin.Game.GENSHIN)
    except genshin.errors.AlreadyClaimed:
        msg = f'今日獎勵已經領過了！'
    except genshin.errors.InvalidCookies:
        msg =  'Cookie已失效，請從Hoyolab重新取得新Cookie'
    except genshin.errors.GenshinException as e:
        msg =  f'簽到失敗：[retcode]{e.retcode} [內容]{e.original}'
    except Exception as e:
        msg =  f'簽到失敗：{e}'
    else:
        msg =  f'今日簽到成功，獲得 {reward.amount}x {reward.name}！'

    await Send(update, msg)

async def notice(update, bot):
    if(isDos(update)): return
    await Send(update, "notice")
    
async def setaccount(update, bot):
    if(isDos(update)): return
    await Send(update, "setaccount")

async def note(update, bot):
    def getTime(time: datetime):
        now = datetime.now(timezone.utc)
        daydiff = time.day - now.day
        if time > now:
            if daydiff == 0:
                days = '今天'
            elif daydiff == 1:
                days = '明天'
            else:
                days = f'{daydiff} 天後'

            return f'{days} {time.strftime("%H:%M")}'
        else:
            return 0
            

    def getResinMsg(data: models.Notes):
        current_resin = data.current_resin
        max_resin = data.max_resin
        resin_recovery_time = getTime(data.resin_recovery_time)
        if resin_recovery_time == 0:
            resin_recovery_time = '樹脂已充滿'
        else:
            resin_recovery_time += ' 恢復'

        return f'當前原粹樹脂：{current_resin} / {max_resin}\n{resin_recovery_time}'

    def getRealmCurrencyMsg(data: models.Notes):
        current_realm_currency = data.current_realm_currency
        max_realm_currency = data.max_realm_currency
        realm_currency_recovery_time = getTime(data.realm_currency_recovery_time)
        if realm_currency_recovery_time == 0:
            realm_currency_recovery_time = '洞天寶錢已充滿'
        else:
            realm_currency_recovery_time += ' 充滿'

        return f'當前洞天寶錢：{current_realm_currency} / {max_realm_currency}\n{realm_currency_recovery_time}'
    
    def getCommissionsMsg(data: models.Notes):
        remaining_commissions = data.max_commissions - data.completed_commissions
        claimed_commission_reward = '已領取' if data.claimed_commission_reward else '未領取'
        return f'每日委託任務：剩餘 {remaining_commissions} 個\n({claimed_commission_reward}獎勵)'

    def getResin_DiscountsMsg(data: models.Notes):
        return f'週本樹脂減半：剩餘 {data.remaining_resin_discounts} 次'

    def getTransformerMsg(data: models.Notes):
        if data.remaining_transformer_recovery_time.total_seconds() < 1:
            msg = '可使用'
        else:
            msg = f'{data.remaining_transformer_recovery_time.days} 天 {data.remaining_transformer_recovery_time.hours} 小時 {data.remaining_transformer_recovery_time.minutes} 分 後充滿'
        return f'參數質變儀　： {msg}'

    def getExpeditionsMsg(data: models.Notes):
        expeditionResult = []
        expedition_finished_count = 0
        for expedition in data.expeditions:
            if expedition.finished:
                expedition_finished_count += 1
                expedition_finish_state = '已完成'
            else:
                expedition_finish_state = f'{getTime(expedition.completion_time)} 完成'

            expeditionResult.append(f'　‧ {expedition.character.name}: {expedition_finish_state}')

        title = f'探索派遣結果：{expedition_finished_count}/{data.max_expeditions}'
        expeditionResult = '\n'.join(expeditionResult)
        return f'{title}\n{expeditionResult}'

    if(isDos(update)): return
    client = getClient(update)
    accounts = await client.get_game_accounts()
    uid = accounts[0].uid
    data = await client.get_genshin_notes(uid)
    
    await Send(update, [
        getResinMsg(data),
        getRealmCurrencyMsg(data),
        getCommissionsMsg(data),
        getResin_DiscountsMsg(data),
        getTransformerMsg(data),
        getExpeditionsMsg(data)
    ])


async def lang(update, bot):
    if(isDos(update)): return
    # await Send(update, "lang")
    
    # cookies = Cookie.Get(getID(update))
    # client = genshin.Client(cookies)
    # accounts = await client.get_game_accounts()
    # data = await client.get_genshin_user(accounts[0].uid)
    # client.claim_daily_reward()

    # for character in data.characters:
    #     await Send(update, character.name + " " + character.weapon.name)

    # await Send(update, genshin_app.getGameAccounts(user_id))

def getClient(update):
    cookies = Cookie.Get(getID(update))

    client = genshin.Client(lang='zh-tw')
    client.set_cookies(cookies)
    client.default_game = genshin.Game.GENSHIN
    
    # accounts = await client.get_game_accounts()
    # data = await client.get_genshin_user(accounts[0].uid)
    return client

async def gift(update, bot):
    await Send(update, "請輸入兌換碼", forceReply = True)
    UserStatus.set(update, UserStatus.RedeemCode)

async def hi(update, bot):
    try:
        await Send(update, f"hi, {update.message.from_user.name}")
    except:
        await Send(update, f"hi, {update.message.from_user.first_name}")
