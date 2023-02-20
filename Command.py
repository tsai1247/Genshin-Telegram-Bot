import asyncio
import re
import json
import shlex
from subprocess import Popen
from typing import Dict

from telegram import Message
from Database.Daily import Daily
from Language import Language
from Logger import appendlog

from Security import isDos
from Variable.Sticker import Sticker
from Variable.String import *
from Variable.UserStatus import UserStatus
from TelegramApi import *
from Database.Cookie import *
from GenshinClient import *

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
    await Reply(update, [
        Language.displaywords.str_cookie_tutorial,
        Language.displaywords.str_cookie_javascript_command
    ])
    UserStatus.set(update, UserStatus.SetCookie)
    

async def repeat(update: Update, bot):
    appendlog(update)
    text = update.message.text.split(' ')
    if len(text) == 1:
        text = '/repeat'
    else:
        text = ' '.join(text[1:])
    await Send(GetGroupID(update), text)

async def daily(update: Update, bot):
    if(isDos(update)): return
    appendlog(update)

    msg = await Claim_Daily_Reward(update)

    buttonTexts = ['open', 'close']
    replyTexts = [   
        json.dumps({
            'status': UserStatus.SetDaily,
            'userID': GetUserID(update),
            'command': i
        }) for i in buttonTexts
    ]
    await ReplyButton(update, msg, 
        [buttonTexts], 
        [replyTexts]
    )

async def note(update: Update, bot):
    if(isDos(update)): return
    appendlog(update)

    message: Message = await Reply(update, "Searching your genshin servers...")
    accountList: Sequence[GenshinAccount] = await GetAccounts(GetClient(update))
    serverList = [account.server for account in accountList]
    buttonTexts = [account.server_name for account in accountList]
    replyTexts = [   
        json.dumps({
            'status': UserStatus.WaitForNotes,
            'userID': GetUserID(update),
            'command': i
        }) for i in serverList
    ]
    await EditButton(message, "Select a server", 
        [buttonTexts], 
        [replyTexts]
    )
    
async def gift(update: Update, bot):    
    if(isDos(update)): return 
    appendlog(update)

    await Reply(update, Language.displaywords.str_enter_redeem_code, forceReply = True)
    UserStatus.set(update, UserStatus.RedeemCode)
    
async def hi(update: Update, bot):
    appendlog(update)
    await Reply(update, f"hi, {update.message.from_user.full_name}")

async def notice(update: Update, bot):
    if(isDos(update)): return
    NotImplemented()

async def setaccount(update: Update, bot):
    if(isDos(update)): return
    NotImplemented()

async def getText(update: Update, bot):
    def getRedeemCode(text: str):
        candidates = re.split('[.,\n\t \r]', text)
        ret = filter(lambda x: 
            x.isascii() and x.isalnum() and not x.isnumeric() and len(x) > 8 and len(x) < 16, candidates)
        ret = list(ret)
        return ret

    if(isDos(update)): return
    appendlog(update)

    if UserStatus.get(update) == UserStatus.SetCookie:
        appendlog(update, 'set cookie')
        cookie = Cookie.Dumps(update.message.text)
        msg = Cookie.Set(GetUserID(update), cookie)
        await Reply(update, msg)
        UserStatus.delete(update)

    elif UserStatus.get(update) == UserStatus.RedeemCode:
        appendlog(update, 'redeemCode')
        text = update.message.text
        userID = GetUserID(update)
        codeList = getRedeemCode(text)
        if len(codeList) == 0:
            await Send(userID , Language.displaywords.str_empty_redeemcode_input)
            return
        
        for code in codeList:
            message: Message = await Send(userID , f'Redeeming {code}: ')
            text = await Redeem_Code(update, code)
            await EditText(message, f"{message.text}\n{text}")
        await Send(userID, Language.displaywords.str_redeemcode_end)
        UserStatus.delete(update)

async def math(update: Update, bot):
    appendlog(update)
    sensitiveList = ['\'', '\"', 'exec', 'eval', 'os', 'import', 'sys', 'app', 'ID', 'Send', 'Reply']
    try:
        text = ' '.join(update.message.text.split()[1:])
        for i in sensitiveList:
            if i.lower() in text.lower():
                await Send(GetUserID(update), "這不是數學")
                return
        fw = open('solution.txt', 'w')
        fw.write(text)
        fw.close()
        a = Popen(shlex.split('python Math.py'))

        timeout = 10
        for cnt in range(timeout):
            await asyncio.sleep(0.5)
            fr = open('solution.txt', 'r')
            sol = fr.readline()
            fr.close()
            if sol == text :
                if cnt+1 == timeout:
                    Send(GetUserID(update), "我算不出來")
                    a.kill()
                    break
                else:
                    continue
            else:
                sol = sol[1:]
                if len(sol) == 0:
                    await ReplySticker(update, Sticker.Capoo_Question)
                    break
                elif len(sol) > text_limit:
                    await Send(GetUserID(update), "答案太長了")
                    break
                else:
                    await Send(GetUserID(update), sol)
                    break
    except Exception as e:
        print(e)
        await Send(GetUserID(update), "我不會數學")

async def callback(update: Update, bot):
    data: Dict = json.loads(update.callback_query.data)
    status, userID, command = data['status'], data['userID'], data['command']
    appendlog(int(userID), 'call back (button clicked)')

    if int(status) == UserStatus.SetDaily:
        appendlog(int(userID), 'switch daily')

        autoDaily = 1 if (command == 'open') else 0
        Daily.Set(userID, autoDaily)
        await Send(int(userID), f"auto-claim the daily rewards: {command}")

    elif int(status) == UserStatus.WaitForNotes:
        status, userID, server = data['status'], data['userID'], data['command']
        message = await Send(userID, 'Loading...')
        text = await Get_Genshin_Notes(userID, server)
        await EditText(message, text[0])
        await Send(userID, text[1:])
