import logging
from urllib.error import HTTPError

from TelegramApi import *
from Language import Language
from Variable.String import *
from Variable.UserStatus import UserStatus

from telegram.ext._callbackcontext import CallbackContext
import genshin
import logging

async def error_handler(update: Update, context: CallbackContext) -> None:
        # about cookie
        if type(context.error) is genshin.errors.InvalidCookies:
            await Reply(update, Language.displaywords.str_InvalidCookies)
            logging.info(f"[例外]: [retcode]{context.error.retcode} [原始內容]{context.error.original} [錯誤訊息]{context.error.msg}")

        # about daily reward
        elif type(context.error) is genshin.errors.AlreadyClaimed:
            buttonTexts = ['open', 'close']
            await ReplyButton(update, Language.displaywords.str_AlreadyClaimed, 
                [buttonTexts], 
                [[f'{UserStatus.SetDaily} {GetUserID(update)} {i}' for i in buttonTexts]], 
            )

        # others
        elif type(context.error) is genshin.errors.DataNotPublic:
            logging.info(f"[例外]: [retcode]{context.error.retcode} [原始內容]{context.error.original} [錯誤訊息]{context.error.msg}")
        elif type(context.error) is genshin.errors.GenshinException:
            logging.warning(f"[例外]: [retcode]{context.error.retcode} [原始內容]{context.error.original} [錯誤訊息]{context.error.msg}")
        elif type(context.error) is HTTPError:
            pass
        else:
            logging.warning(f"[例外]: [錯誤訊息]{context.error}")

        UserStatus.delete(update)