import sqlite3
from typing import Union

from Variable.String import *

from telegram import Update

class Language:
    languageMap = {'en': en(), 'zhTW': zhTW()}
    displaywords = languageMap['zhTW']

    @staticmethod
    def Get(userID: int):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select language from Language where userID = ?", [userID])
        data = cur.fetchone()
        if(data == None):
            data = 'zhTW'
        else:
            data = data[0]
        cur.close()
        sql.close()

        return data

    @staticmethod
    def Set(ID: int, language: str):
        sql = sqlite3.connect('KaTsu.db')
        cur = sql.cursor()
        cur.execute("select userID from Language where userID = ?", [ID])
        data = cur.fetchone()
        if(data == None):   # insert
            cur.close()
            cur = sql.cursor()
            cur.execute("insert into Language values(?, ?)", [ID, language])
            sql.commit()
        else:               # update
            cur.close()
            cur = sql.cursor()
            cur.execute("update Language set language = ? \
                         where userID = ?", [language, ID])
            sql.commit()
        cur.close()
        sql.close()

    def SetLang(userID: Union[Update, int]):
        if type(userID) is Update:
            userID: int = userID.message.from_user.id
        cur = Language.Get(userID)
        Language.displaywords = Language.languageMap[cur]