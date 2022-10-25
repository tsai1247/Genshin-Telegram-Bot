
from typing import Union
from telegram import Update
from TelegramApi import GetUserID


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
