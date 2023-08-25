# 事件倒數Discord Bot
一個每天會自動發送事件倒數訊息至指定伺服器之指定頻道的Discord Bot，且會提及指定的身分組。


## 簡介

本DC Bot所需檔案之如下，並附上各檔案的說明。
* **bot_zh.py**</br>
中文版的Bot的主程式碼，請注意不要選成`bot.py`，那是英文版的。
* **keep_alive.py**</br>
用於生成運行視窗，請見下方「**讓Discord Bot保持運行**」。
* **date.json**</br>
用於儲存所有事件之資料（事件名稱和日期）。
* **send.txt**</br>
用於紀錄上次傳送通知的時間。


## 使用說明
運行機器人之前，請先設定好`bot_zh.py`，步驟如下：
1. 將`TOKEN`填入你的Discord Bot的TOKEN。</br>
2. 取得要發送訊息的伺服器ID和頻道ID，分別填入`GUILD_ID`和`CHANNEL_ID`。
3. 將要提及的身分組名稱填入`ROLE_NAME`。
4. 設定訊息傳送時間，預設是每日0點整。由左至右四個數值分別為***時***、***分***、***秒***、***毫秒***。
5. 設定時間檢查間隔，預設是每60秒檢查一次是否到達傳送訊息的時間。

設定完成後，運行`bot_zh.py`，就可以開始使用機器人啦！


## 指令介紹
* **查詢指令**`!help command`</br>
查詢某個指令的使用方式，例如`!help add`。
* **測試運行**`!test`</br>
測試機器人運行狀態，如果正常運行會回傳`運作中`。
* **新增事件**`!add yyyy-mm-dd name`</br>
新增一個名為name的事件，例如`!add 2023-01-01 生日`。
* **刪除事件**`!delete name`</br>
刪除名為name的事件，例如`!delete 生日`。
* **查看事件**`!check`</br>
查看現在有哪些事件。


## 讓Discord Bot保持運行

> 可參考以下教學
> * [[Proladon] Code a discord bot - 如何讓Discord Bot 24小時在線](https://www.youtube.com/watch?v=UT1h9un4Cpo)
> * [Building a Discord bot with Python and Replit](https://docs.replit.com/tutorials/python/build-basic-discord-bot-python)

### 將Bot放在Replit上運行
1. 進入[Replit](https://replit.com/)並註冊帳號
2. 點選側欄的`+ Create Repl`，**Template**選擇`Python`，**Title**打上專案名稱，按下`+ Create Repl`
3. 將`bot-zh.py`的程式碼複製到`main.py`
4. 點選側欄**Files**的`⋮`，按下`Upload file`，匯入*date.json*、*keep_alive.py*、*send.txt*三個檔案
5. 儲存後按下`Run`的按鈕，應會出現顯示`Hello. I am alive!`的視窗
6. 複製該視窗上方的網址，例如`https://bot.username.repl.co`

### 監控Bot確保其持續運作
1. 進入[UptimeRobot](https://uptimerobot.com/)並註冊帳號
2. 點擊左上角的`+ Add New Monitor`新增監控器
3. **Monitor Type**選擇`HTTP(s)`，**Friendly Name**打上專案名稱，**URL (or IP)** 貼上剛剛複製的網址，**Monitoring Interval**選擇`every 5 minutes`(免費版可選擇的最短監控間隔時間)
4. 設定完成後按下`Create Monitor`