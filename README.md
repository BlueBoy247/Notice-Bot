# Event Countdown Discord Bot
 A Discord Bot that automatically sends daily event countdown messages to a specified channel on a designated server and mentions a specific role.
 
[Chinese version(中文版)](https://github.com/BlueBoy247/Event-Countdown-Discord-Bot/blob/main/README_zh.md)


## Introduction

Here are the required files for this Discord bot, along with descriptions for each file:
* **bot.py**</br>
The main code for the bot in English.
* **keep_alive.py**</br>
Used to create a runtime window for the bot. Refer to the section "**Keeping the Discord Bot Running 24/7**" below.
* **date.json**</br>
Used to save data for all events, including event names and dates.
* **send.txt**</br>
Used to record the last time a notification was sent.
 

## Tutorial
Before running the bot, please configure `bot.py` using the following steps:

1. Fill in your Discord Bot's TOKEN in the `TOKEN`.
2. Obtain the server ID and channel ID where you want to send messages. Fill in `GUILD_ID` and `CHANNEL_ID` respectively.
3. Enter the role name you want to mention in the `ROLE_NAME`.
4. Set the message sending time. The default is every day at midnight. The four values from left to right represent ***hour***, ***minute***, ***second***, and ***millisecond***.
5. Set the time interval for checking. The default is to check every 60 seconds whether it's time to send the message.

After configuration, run `bot.py`, and you can start using the bot!

## Command Description
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


## Keep the Discord Bot running 24/7

> You can refer to the following tutorials:
> * [24/7 FREE Discord Bot Hosting - No Down Time | Repl it, UpTimeRobot | Part 2](https://www.youtube.com/watch?v=-5ptk-Klfcw)
> * [Building a Discord bot with Python and Replit](https://docs.replit.com/tutorials/python/build-basic-discord-bot-python)

### Run the Bot on Replit
1. Go to replit.com and create an account.
2. Click on the `+ Create Repl` button in the sidebar. Choose the `Python` template, enter your project name in the Title field, and click `+ Create Repl`.
3. Copy the code from `bot-en.py` and paste it into `main.py`.
4. Click the `⋮` icon in the sidebar next to `Files`, then select `Upload file`. Upload the `date.json`, `keep_alive.py`, and `send.txt` files.
5. After uploading, click the `Run` button. A window should appear displaying `Hello. I am alive!`.
6. Copy the URL from the top of that window, for example, `https://bot.username.repl.co`.

### Use UptimeRobot to monitor the Bot 
1. Go to uptimerobot.com and create an account.
2. Click on the `+ Add New Monitor` option at the top left to create a new monitor.
3. Choose `HTTP(s)` as the `Monitor Type`, enter your project name in the `Friendly Name` field, paste the URL you copied earlier into the `URL (or IP)` field, and select `every 5 minutes` as the `Monitoring Interval` (the shortest monitoring interval available in the free version).
4. Once you've configured these settings, click `Create Monitor`.