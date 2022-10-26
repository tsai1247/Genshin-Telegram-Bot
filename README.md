# 原神 Telegram Bot

歡迎將本專案所有或部分程式碼放入你自己的機器人中，只需要在你專案的網頁、README 或任何公開的說明文件放入本專案的作者與連結

Feel free to take all or part of the code to your own bot, just put the author and URL of this project in your project's website, README or any public documentation.

## 銘謝 Thanks
此專案部分程式碼與說明參考 [KT-Yeh 的專案](https://github.com/KT-Yeh/Genshin-Discord-Bot)，並直接引用 [thesadru提供的套件](https://github.com/thesadru/genshin.py)。

The repository references [KT-Yeh's repo](https://github.com/KT-Yeh/Genshin-Discord-Bot), and uses [package from thesadru](https://github.com/thesadru/genshin.py).  Thanks a lot.


## 簡介
* 可以在Telegram上直接使用此bot，來完成：
  - 查詢即時便箋，包含樹脂、洞天寶錢、參數質變儀、探索派遣完成時間...等
  - Hoyolab 使用兌換碼
  - Hoyolab 自動簽到
* 未來將有以下功能：
  - 自動檢查樹脂，並當樹脂將滿時發送提醒
  - 加入"群組"功能，可以一次對"群組"內的所有玩家使用兌換碼
  - 若cookie經常失效，提供帳號密碼的暫存，讓bot自行抓取cookie
    - (開發者這邊僅能口頭保證不會對此帳號密碼做取得cookie之外的用途，若不信任開發者，可以選擇[自行架設機器人](#自己安裝--架設機器人))

## 使用方式
- 點擊 [連結](https://t.me/KaTsuGenshinBot) ，或在 Telegram 中直接查詢 @KaTsuGenshinBot
- 使用 `/help` 指令來得到詳細的幫助，或僅輸入 `/` 可以看到所有指令與簡易說明
- 第一次使用請記得先用 `/cookie` 指令設定cookie

## 自己安裝 & 架設機器人
### 注意
* 此專案使用到 telegram 官方提供的 pre-release 套件，可能會出現未預期錯誤。若有問題再煩請告知，謝謝。
### 取得自己的bot
1. 與 [BotFather](https://t.me/BotFather)傳訊息，使用 `/newbot` 指令來獲得新的bot
2. 得到新的bot後，重點資訊請記下：
   - 你的bot的連結，確認可以傳訊息給你的bot
   - bot_token，一串由 `[1-9]+:[A-Za-z0-9_]+` 組成的字符串

### 本地端
1. 下載 [本專案的壓縮檔](https://github.com/tsai1247/Genshin-Telegram-Bot/archive/refs/heads/master.zip)並解壓縮，或用其他方法將 [本專案](https://github.com/tsai1247/Genshin-Telegram-Bot/) Clone至本地
2. 下載並安裝 Python（版本 3.8 以上）: https://www.python.org/downloads/
3. 在專案資料夾（Genshin-Telegram-Bot）內，用文字編輯器開啟 `.env.example` 檔案，將得到的bot_token取代掉內容的`{...}`，輸入完後會類似：`TELEGRAM_TOKEN='1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ'`
4. 將 `.env.example` 檔案名稱另存為 `.env`
5. 在專案資料夾內開啟 cmd 或 powershell，輸入底下命令安裝相關套件：
```
pip3 install -U -r requirements.txt
```
6. 輸入底下命令，開始運行機器人
```
python .\main.py
```
