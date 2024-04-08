# Notice Bot
English | [繁體中文](./README-zht.md)

A Discord Bot that automatically sends daily event countdown messages to a specified channel on a designated server and mentions a specific role.


## Introduction
Here are the required files for this Discord bot, along with descriptions for each file:
* **bot.py**</br>
The main code for the bot in English.
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