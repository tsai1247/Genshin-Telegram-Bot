# coding=utf-8
from genshin.models import Notes
from datetime import datetime, timezone

class en():
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
    str_empty_redeemcode_input = 'Get no code from your input'
    str_redeemcode_end = 'End of redemption'

    str_cookie_successful = 'cookie is updated'
    str_cookie_fail = 'update cookie...failed, please check the cookie format'

    str_redeem_cooldown_waiting = 'redeem system cooldown. '
    
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
        if realm_currency_recovery_time == None:
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
    str_InvalidCookies_when_Daiily = 'Invalid cookie when claim daily reward. please get a new one from Hoyolab.'
    str_RedemptionClaimed = 'The code has been used.'
    str_RedemptionInvalid = 'Invalid redemption code.'
    str_RedemptionException = 'Redemption failed.'

    str_redeem_successful = "Successful."
    str_AlreadyClaimed = 'Today\'s reward has been claimed!'
    