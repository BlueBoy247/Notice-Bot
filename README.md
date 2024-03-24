# Notice Bot
一個每天會自動發送事件倒數訊息至指定伺服器之指定頻道的DC Bot，且會提及指定的身分組。

A Discord Bot that automatically sends daily event countdown messages to a specified channel on a designated server and mentions a specific role.

> **中文版在下方！**


## English
### Introduction
Here are the required files for this Discord bot, along with descriptions for each file:
* **bot.py**</br>
The main code for the bot in English.
* **date.json**</br>
Used to save data for all events, including event names and dates.
* **send.txt**</br>
Used to record the last time a notification was sent.
 

### Tutorial
Before running the bot, please configure `bot.py` using the following steps:

1. Fill in your Discord Bot's TOKEN in the `TOKEN`.
2. Obtain the server ID and channel ID where you want to send messages. Fill in `GUILD_ID` and `CHANNEL_ID` respectively.
3. Enter the role name you want to mention in the `ROLE_NAME`.
4. Set the message sending time. The default is every day at midnight. The four values from left to right represent ***hour***, ***minute***, ***second***, and ***millisecond***.
5. Set the time interval for checking. The default is to check every 60 seconds whether it's time to send the message.

After configuration, run `bot.py`, and you can start using the bot!

### Command Description
* **help** `!help command`</br>
Inquire about the syntax of a specific command.</br>
Example: `!help add`
* **test** `!test`</br>
Test the bot's running status, if it's running correctly, it will return `Alive`.
* **add** `!add yyyy-mm-dd name`</br>
Add an event named "name".</br>
Example: `!add 2023-01-01 Birthday`
* **delete** `!delete name`</br>
Delete the event named "name".</br>
Example: `!delete Birthday`
* **check** `!check`</br>
Query the currently existing events.


## 中文 Chinese(zh-TW)
### 簡介
本DC Bot所需檔案之如下，並附上各檔案的說明。
* **bot_zh.py**</br>
中文版的Bot的主程式碼，請注意不要選成`bot.py`，那是英文版的。
* **date.json**</br>
用於儲存所有事件之資料（事件名稱和日期）。
* **send.txt**</br>
用於紀錄上次傳送通知的時間。


### 使用說明
運行機器人之前，請先設定好`bot_zh.py`，步驟如下：
1. 將`TOKEN`填入你的Discord Bot的TOKEN。</br>
2. 取得要發送訊息的伺服器ID和頻道ID，分別填入`GUILD_ID`和`CHANNEL_ID`。
3. 將要提及的身分組名稱填入`ROLE_NAME`。
4. 設定訊息傳送時間，預設是每日0點整。由左至右四個數值分別為***時***、***分***、***秒***、***毫秒***。
5. 設定時間檢查間隔，預設是每60秒檢查一次是否到達傳送訊息的時間。

設定完成後，運行`bot_zh.py`，就可以開始使用機器人啦！


### 指令介紹
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