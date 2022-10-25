import sqlite3
from typing import Union

from Variable.String import *

from telegram import Update

class Language:
    languageMap = {'en': en()}
    displaywords = languageMap['en']
