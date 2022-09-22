# coding=utf-8
from genshin.models import Notes
from datetime import datetime, timezone

str_welcome = [
    "嗨",
    "我可以幫你的原神每日簽到以及提醒資源的狀況",
    "使用 /help 來取得更多資訊"
]

str_help = [
    "你可能會想要：",
    "0. 第一次使用此bot時，使用 /cookie 設定你的 cookie。\n" + \
            "  cookie 可以讓 bot 協助你取得 hoyolab 上的資訊\n" + \
            "  (請放心，持有 cookie並無法修改你的任何遊戲進度)",
    "1. 使用 /daily 開啟或關閉原神每日簽到，協助你確實領到每日簽到獎勵",
    "2. 使用 /notice 在樹脂將滿時、洞天寶錢將滿時、探索完成時提醒你",
    "3. 使用 /note 即時確認樹脂、洞天寶錢、探索狀態等數值",
    "4. 使用 /account 在你的 cookie 因為不明原因頻繁更換時，你可以直接提供 hoyolab 的帳號密碼給 bot ，讓 bot 來主動更新 cookie。\n" + \
            "(請注意：若你不信任此 bot 的提供者，請勿使用此指令來交付帳號密碼。你當然可以自行在 hoyolab 上修改帳號密碼使此功能失效。)"
]

str_cookie_tutorial = \
    "步驟一： 使用瀏覽器進入 https://www.hoyolab.com/ ，並且登入\n" + \
    "步驟二： 將網址欄清空，輸入java後貼上下方文字，確認文字開頭為「javascript:」，並沒有多餘的引號或空格後，按下Enter\")\n" + \
    "步驟三： 將網頁顯示的文字全選，複製後貼到此聊天室\n" + \
    "更詳細的內容請參閱 https://genshin.xiaokuai.tk/cookie幫助/"

str_cookie_javascript_command = \
    "script:d=document.cookie; c=d.includes('account_id') || alert('過期或無效的Cookie,請先登出帳號再重新登入!'); c && document.write(d)"


def getStrftime(time: datetime):
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
        return None

def GetResinMsg(data: Notes):
    current_resin = data.current_resin
    max_resin = data.max_resin
    resin_recovery_time = getStrftime(data.resin_recovery_time)
    if resin_recovery_time == None:
        resin_recovery_time = '樹脂已充滿'
    else:
        resin_recovery_time += ' 恢復'

    return f'當前原粹樹脂：{current_resin} / {max_resin}\n{resin_recovery_time}'

def GetRealmCurrencyMsg(data: Notes):
    current_realm_currency = data.current_realm_currency
    max_realm_currency = data.max_realm_currency
    realm_currency_recovery_time = getStrftime(data.realm_currency_recovery_time)
    if realm_currency_recovery_time == 0:
        realm_currency_recovery_time = '洞天寶錢已充滿'
    else:
        realm_currency_recovery_time += ' 充滿'

    return f'當前洞天寶錢：{current_realm_currency} / {max_realm_currency}\n{realm_currency_recovery_time}'

def GetCommissionsMsg(data: Notes):
    remaining_commissions = data.max_commissions - data.completed_commissions
    claimed_commission_reward = '已領取' if data.claimed_commission_reward else '未領取'
    return f'每日委託任務：剩餘 {remaining_commissions} 個\n({claimed_commission_reward}獎勵)'

def GetResin_DiscountsMsg(data: Notes):
    return f'週本樹脂減半：剩餘 {data.remaining_resin_discounts} 次'

def GetTransformerMsg(data: Notes):
    if data.remaining_transformer_recovery_time.total_seconds() < 1:
        msg = '可使用'
    else:
        msg = f'{data.remaining_transformer_recovery_time.days} 天 {data.remaining_transformer_recovery_time.hours} 小時 {data.remaining_transformer_recovery_time.minutes} 分 後充滿'
    return f'參數質變儀　： {msg}'

def GetExpeditionsMsg(data: Notes):
    expeditionResult = []
    expedition_finished_count = 0
    for expedition in data.expeditions:
        if expedition.finished:
            expedition_finished_count += 1
            expedition_finish_state = '已完成'
        else:
            expedition_finish_state = f'{getStrftime(expedition.completion_time)} 完成'

        expeditionResult.append(f'　‧ {expedition.character.name}: {expedition_finish_state}')

    title = f'探索派遣結果：{expedition_finished_count}/{data.max_expeditions}'
    expeditionResult = '\n'.join(expeditionResult)
    return f'{title}\n{expeditionResult}'

