import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import datetime
import pytz
from keep_alive import keep_alive
import json

TOKEN = '0000' # 機器人的TOKEN
GUILD_ID = 0000  # Discord 伺服器的 ID
CHANNEL_ID = 0000  # 訊息發送目標頻道的ID
ROLE_NAME = 'ROLE' # 要提及的身分組名稱

# 設定訊息傳送時間 (hh:mm:ss.ff)
set_hour, set_minute, set_second, set_microsecond = 0, 0, 0, 0 # 00:00:00.00

# 設定每幾秒檢查一次是否到達傳送訊息的時間
interval = 60

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# 載入date.json
def load_dates():
  try:
    with open('date.json', 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return {}


# 儲存date.json
def save_dates(dates):
  with open('date.json', 'w') as f:
    json.dump(dates, f)


# 取得目標身分組
def get_target_role(guild):
  return discord.utils.get(guild.roles, name=ROLE_NAME)


# 設定時區
set_time_zone = 'Asia/Taipei' # UTC+8
timezone = pytz.timezone(set_time_zone)


# 讀取上次傳送通知的日期
def load_last_notification_date():
  try:
    with open('send.txt', 'r') as f:
      return f.read().strip()
  except FileNotFoundError:
    return None


# 更新上次傳送通知的日期
def update_last_notification_date(date):
  with open('send.txt', 'w') as f:
    f.write(date)


# 在傳送通知前檢查日期
async def check_notification_date(channel):
  last_date_str = load_last_notification_date()
  current_date = datetime.datetime.now(timezone).date()

  if last_date_str is None or last_date_str != current_date.strftime('%Y-%m-%d'):
    update_last_notification_date(current_date.strftime('%Y-%m-%d'))
    return True
  else:
    return False
  

# 傳送通知
async def check_reminders(channel, days_dict):
  now = datetime.datetime.now(timezone).date()
  target_role = get_target_role(channel.guild)
  notice_message = f'{target_role.mention}\n'
  for name, date_str in days_dict.items():
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    days_left = (date_obj - now).days
    if days_left == 0:
      notice_message += f"今天是{name}\n！"
    elif days_left > 0:
      notice_message += f'距離 {name} 還有 {days_left} 天！\n'
  await channel.send(notice_message)


@bot.event
async def on_ready():
  print('The bot has successfully logged in.')

  # 設定機器人的status
  bot_status = "遊戲"
  activity = discord.Game(name=bot_status)
  await bot.change_presence(activity=activity)

  # 取得目標伺服器和頻道
  guild = bot.get_guild(GUILD_ID)
  channel = guild.get_channel(CHANNEL_ID)

  # 載入現有的事件
  days_dict = load_dates()

  while True:
    now = datetime.datetime.now(timezone)
    target_time = now.replace(hour=set_hour, minute=set_minute, second=set_second, microsecond=set_microsecond)

    if now >= target_time:
      # 檢查今日的倒數通知是否尚未傳送
      should_send_notification = await check_notification_date(channel)
      if should_send_notification:
        # 傳送倒數通知
        await check_reminders(channel, days_dict)
        pass

      # 計算下一次（隔天）傳送通知的時間
      next_target_time = target_time + datetime.timedelta(days=1)

      # 計算下一次檢查現在時間的時間
      sleep_seconds = (next_target_time - now).total_seconds()
      await asyncio.sleep(sleep_seconds)

    else:
      # 未到指定的通知時間，繼續等待
      await asyncio.sleep(interval)


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  await bot.process_commands(message)


@bot.command()
async def test(ctx):
  test_message = "運作中"
  await ctx.send(test_message)


@bot.command()
async def add(ctx, date_str=None, name=None):
  if date_str is None or name is None:
    await ctx.send('請提供事件日期和名稱')
    return

  try:
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    # 載入現有事件
    days_dict = load_dates()

    # 新增事件
    days_dict[name] = str(date_obj)

    # 儲存date.json
    save_dates(days_dict)

    await ctx.send(f'已新增事件： {name} - {date_obj}')
  except ValueError:
    await ctx.send('請使用正確的日期格式 (YYYY-MM-DD)')


@bot.command()
async def delete(ctx, name):
  # 載入現有事件
  days_dict = load_dates()

  if name in days_dict:
    # 刪除事件
    del days_dict[name]

    # 儲存date.json
    save_dates(days_dict)

    await ctx.send(f'已移除事件： {name}')
  else:
    await ctx.send(f'找不到名為 {name} 的事件')


@bot.command()
async def check(ctx):
  # Load existing events
  days_dict = load_dates()
  if days_dict:
    check_message = "目前的計時器設定如下：\n"
    for name, date_obj in days_dict.items():
      check_message += f"{name}: {date_obj}\n"
    await ctx.send(check_message)
  else:
    await ctx.send("目前沒有任何計時器設定。")


# Customize the bot's help command
class CustomHelpCommand(commands.DefaultHelpCommand):
  
  def get_command_signature(self, command):
    return f'{self.clean_prefix}{command.qualified_name} {command.signature}'
  
  @property
  def clean_prefix(self):
    return self.context.bot.command_prefix
  
  async def send_command_help(self, command):

    embed = discord.Embed(title='指令幫助',
                          description=command.help,
                          color=discord.Color.green())
    embed.add_field(name='使用語法',
                    value=self.get_command_signature(command),
                    inline=False)
    await self.get_destination().send(embed=embed)
    
  async def send_bot_help(self, mapping):
    all_command = {
      '查詢指令': '`!help command`\n查詢某個指令的使用方式\n例如：`!help add`',
      '測試運行': '`!test`\n測試機器人運行狀態',
      '新增計時器': '`!add yyyy-mm-dd name`\n新增一個名為 name 的計時器\n例如：`!add 2023-01-01 生日`',
      '刪除計時器': '`!delete name`\n刪除名為 name 的計時器\n例如：`!delete 生日`',
      '查詢計時器': '`!check`\n查詢現在有哪些倒數計時器',
    }
    embed = discord.Embed(title='教程',
                          description='以下為本Discord Bot的所有指令與使用教學',
                          color=discord.Color.green())
    count = 0
    for k, v in all_command.items():
      if count % 2 == 0:
        embed.add_field(name="", value="", inline=False)
      embed.add_field(name=k, value=v, inline=True)
      count += 1
    await self.get_destination().send(embed=embed)
    
bot.help_command = CustomHelpCommand()


keep_alive()


bot.run(TOKEN)
