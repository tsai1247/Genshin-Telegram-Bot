# coding=utf-8
from genshin.models import Notes
from datetime import datetime, timezone
from abc import abstractmethod

class Lang():
    def __init__(self):
        pass

    str_welcome = ''
    str_help = ''
    
    str_enter_cookie = ''
    str_cookie_tutorial = ''
    str_cookie_javascript_command = ''
    str_daily_successful = ''
    str_enter_redeem_code = ''
    str_cookie_successful = ''

    @abstractmethod
    def getStrftime(self, time: datetime):
        pass

    @abstractmethod
    def GetResinMsg(self, data: Notes):
        pass

    @abstractmethod
    def GetRealmCurrencyMsg(self, data: Notes):
        pass

    @abstractmethod
    def GetCommissionsMsg(self, data: Notes):
        pass

    @abstractmethod
    def GetResin_DiscountsMsg(self, data: Notes):
        pass

    @abstractmethod
    def GetTransformerMsg(self, data: Notes):
        pass

    @abstractmethod
    def GetExpeditionsMsg(self, data: Notes):
        pass

    # error message
    str_InvalidCookies = ''
    str_RedemptionClaimed = ''
    str_RedemptionInvalid = ''
    str_RedemptionException = ''

    str_AlreadyClaimed = ''

    str_switch_lang_success = ''
    str_current_lang = ''

class zhTW(Lang):
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

    str_enter_cookie = '請輸入你的cookie：'

    str_cookie_tutorial = \
        "步驟一： 使用瀏覽器進入 https://www.hoyolab.com/ ，並且登入\n" + \
        "步驟二： 將網址欄清空，輸入java後貼上下方文字，確認文字開頭為「javascript:」，並沒有多餘的引號或空格後，按下Enter\")\n" + \
        "步驟三： 將網頁顯示的文字全選，複製後貼到此聊天室\n" + \
        "更詳細的內容請參閱 https://genshin.xiaokuai.tk/cookie幫助/"
    
    str_cookie_javascript_command = "script:d=document.cookie; c=d.includes('account_id') || alert('過期或無效的Cookie,請先登出帳號再重新登入!'); c && document.write(d)"

    str_daily_successful = '今日簽到成功，獲得'

    str_enter_redeem_code = '請輸入兌換碼'

    str_cookie_successful = 'cookie已更新'

    def getStrftime(self, time: datetime):
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

    def GetResinMsg(self, data: Notes):
        current_resin = data.current_resin
        max_resin = data.max_resin
        resin_recovery_time = self.getStrftime(data.resin_recovery_time)
        if resin_recovery_time == None:
            resin_recovery_time = '樹脂已充滿'
        else:
            resin_recovery_time += ' 恢復'

        return f'當前原粹樹脂：{current_resin} / {max_resin}\n{resin_recovery_time}'

    def GetRealmCurrencyMsg(self, data: Notes):
        current_realm_currency = data.current_realm_currency
        max_realm_currency = data.max_realm_currency
        realm_currency_recovery_time = self.getStrftime(data.realm_currency_recovery_time)
        if realm_currency_recovery_time == 0:
            realm_currency_recovery_time = '洞天寶錢已充滿'
        else:
            realm_currency_recovery_time += ' 充滿'

        return f'當前洞天寶錢：{current_realm_currency} / {max_realm_currency}\n{realm_currency_recovery_time}'

    def GetCommissionsMsg(self, data: Notes):
        remaining_commissions = data.max_commissions - data.completed_commissions
        claimed_commission_reward = '已領取' if data.claimed_commission_reward else '未領取'
        return f'每日委託任務：剩餘 {remaining_commissions}/{data.max_commissions} 個\n({claimed_commission_reward}獎勵)'

    def GetResin_DiscountsMsg(self, data: Notes):
        return f'週本樹脂減半：剩餘 {data.remaining_resin_discounts}/{data.max_resin_discounts} 次'

    def GetTransformerMsg(self, data: Notes):
        if data.remaining_transformer_recovery_time.total_seconds() < 1:
            msg = '可使用'
        else:
            msg = f'{data.remaining_transformer_recovery_time.days} 天 {data.remaining_transformer_recovery_time.hours} 小時 {data.remaining_transformer_recovery_time.minutes} 分 後充滿'
        return f'參數質變儀　： {msg}'

    def GetExpeditionsMsg(self, data: Notes):
        expeditionResult = []
        expedition_finished_count = 0
        for expedition in data.expeditions:
            if expedition.finished:
                expedition_finished_count += 1
                expedition_finish_state = '已完成'
            else:
                expedition_finish_state = f'{self.getStrftime(expedition.completion_time)} 完成'

            expeditionResult.append(f'　‧ {expedition.character.name}: {expedition_finish_state}')

        title = f'探索派遣結果：{expedition_finished_count}/{data.max_expeditions}'
        expeditionResult = '\n'.join(expeditionResult)
        return f'{title}\n{expeditionResult}'

    # error message
    str_InvalidCookies = 'Cookie已失效，請從Hoyolab重新取得新Cookie'
    str_RedemptionClaimed = '兌換碼已被使用'
    str_RedemptionInvalid = '無效的兌換碼'
    str_RedemptionException = '兌換失敗'

    str_AlreadyClaimed = '今日獎勵已經領過了！'
    
    str_switch_lang_success = '成功切換語言為：'
    str_current_lang = '當前語言：'

class en(Lang):
    str_welcome = [
        "Hi",
        "I can help you to claim daily rewards, check the resouces and so on.",
        "/help for more information."
    ]

    str_help = [
        "You might want to...",
        "In the beginning, use /cookie to set your cookie\n" + \
            "  which allows bot to get the information on Hoyolab.\n" + \
            "  (Rest assured that it's impossible to modify your game progress with cookie.)",
        "1. Use /daily to en/disable the work of claiming daily reward automatically.",
        "2. Use /notice to remind you when resin or realm currency is about to full.",
        "3. Use /note to watch the Real-Time Notes",
        "4. Use /account only when your cookie is frequently changed by unknown reasons." + \
            "(Please note: never provide your account and password if you don't trust this bot.)"
    ]

    str_enter_cookie = 'Enter your hoyolab cookie：'

    str_cookie_tutorial = \
        "Step 1: Use a browser to enter https://www.hoyolab.com/, and login.\n" + \
        "Step 2: Clear the URL bar, type \"java\" and paste the text below\n" + \
        "Step 3: Make sure the text in URL bar start with \"javascript\" and no extra quotation marks or spaces, and press Enter\"\n" + \
        "Step 4: Select all the text on the webpage, and paste it into this chat room.\n" + \
        "For more details, see https://genshin.xiaokuai.tk/cookie幫助/"

    str_cookie_javascript_command = "script:d=document.cookie; c=d.includes('account_id') || alert('Expired or invalid cookie, please log out and log in again!'); c && document.write(d)"
    
    str_daily_successful = 'Successful. Get'

    str_enter_redeem_code = 'Enter the code'
    
    str_cookie_successful = 'cookie is updated'
    
    def getStrftime(self, time: datetime):
        now = datetime.now(timezone.utc)
        daydiff = time.day - now.day
        if time > now:
            if daydiff == 0:
                days = 'today'
            elif daydiff == 1:
                days = 'tomorrow'
            else:
                days = f'after {daydiff} days,'

            return f'{days} {time.strftime("%H:%M")}'
        else:
            return None

    def GetResinMsg(self, data: Notes):
        current_resin = data.current_resin
        max_resin = data.max_resin
        resin_recovery_time = self.getStrftime(data.resin_recovery_time)
        if resin_recovery_time == None:
            resin_recovery_time = 'Origin Resin is full.'
        else:
            resin_recovery_time = f'Origin Resin will be full at {resin_recovery_time}'

        return f'Origin Resin: {current_resin} / {max_resin}\n{resin_recovery_time}'

    def GetRealmCurrencyMsg(self, data: Notes):
        current_realm_currency = data.current_realm_currency
        max_realm_currency = data.max_realm_currency
        realm_currency_recovery_time = self.getStrftime(data.realm_currency_recovery_time)
        if realm_currency_recovery_time == 0:
            realm_currency_recovery_time = 'Realm Currency is full.'
        else:
            realm_currency_recovery_time = f'Realm Currency will be full at {realm_currency_recovery_time}'

        return f'Realm Currency: {current_realm_currency} / {max_realm_currency}\n{realm_currency_recovery_time}'

    def GetCommissionsMsg(self, data: Notes):
        remaining_commissions = data.max_commissions - data.completed_commissions
        claimed_commission_reward = 'claimed' if data.claimed_commission_reward else 'not claimed'
        return f'Daily Commissions: {remaining_commissions}/{data.max_commissions} remaining\n(the reward is {claimed_commission_reward}.)'

    def GetResin_DiscountsMsg(self, data: Notes):
        return f'Resin Cost-Halving toward Enemies: {data.remaining_resin_discounts}/{data.max_resin_discounts} remaining.'

    def GetTransformerMsg(self, data: Notes):
        if data.remaining_transformer_recovery_time.total_seconds() < 1:
            msg = 'cooldown ended.'
        else:
            msg = f'{data.remaining_transformer_recovery_time.days} days {data.remaining_transformer_recovery_time.hours} hours {data.remaining_transformer_recovery_time.minutes} minutes remaining'
        return f'Parametric Transformer: {msg}'

    def GetExpeditionsMsg(self, data: Notes):
        expeditionResult = []
        expedition_finished_count = 0
        for expedition in data.expeditions:
            if expedition.finished:
                expedition_finished_count += 1
                expedition_finish_state = 'Completed'
            else:
                expedition_finish_state = f'{self.getStrftime(expedition.completion_time)}'

            expeditionResult.append(f'　‧ {expedition.character.name}: {expedition_finish_state}')

        title = f'Expedition: {expedition_finished_count}/{data.max_expeditions}'
        expeditionResult = '\n'.join(expeditionResult)
        return f'{title}\n{expeditionResult}'

    # error message
    str_InvalidCookies = 'Invalid cookie, please get a new one from Hoyolab.'
    str_RedemptionClaimed = 'The code has been used.'
    str_RedemptionInvalid = 'Invalid redemption code.'
    str_RedemptionException = 'Redemption failed.'

    str_AlreadyClaimed = 'Today\'s reward has been claimed!'
    
    str_switch_lang_success = 'The language is switched to '
    str_current_lang = 'Current language: '
