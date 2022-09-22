import logging

from TelegramApi import *

from telegram.ext._callbackcontext import CallbackContext
import genshin

async def error_handler(update: Update, context: CallbackContext) -> None:
        # about cookie
        if type(context.error) is genshin.errors.InvalidCookies:
            await Send(update, 'Cookie已失效，請從Hoyolab重新取得新Cookie')
            logging.info(f"[例外]: [retcode]{context.error.retcode} [原始內容]{context.error.original} [錯誤訊息]{context.error.msg}")
        
        # about redeem code
        elif type(context.error) is genshin.RedemptionCooldown:
            raise context.error
        elif type(context.error) is genshin.RedemptionClaimed:
            await Send(update, '兌換碼已被使用')
        elif type(context.error) is genshin.RedemptionInvalid:
            await Send(update, '無效的兌換碼')
        elif type(context.error) is genshin.RedemptionException:
            await Send(update, f'兌換失敗：[retcode]{context.error.retcode} [內容]{context.error.original}')

        # about daily reward
        elif type(context.error) is genshin.errors.AlreadyClaimed:
            await Send(update, '今日獎勵已經領過了！')

        # others
        elif type(context.error) is genshin.errors.DataNotPublic:
            logging.info(f"[例外]: [retcode]{context.error.retcode} [原始內容]{context.error.original} [錯誤訊息]{context.error.msg}")
        elif type(context.error) is genshin.errors.GenshinException:
            logging.warning(f"[例外]: [retcode]{context.error.retcode} [原始內容]{context.error.original} [錯誤訊息]{context.error.msg}")
        else:
            logging.warning(f"[例外]: [錯誤訊息]{context.error}")
        
        