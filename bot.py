import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import datetime
import pytz
from keep_alive import keep_alive
import json

TOKEN = '0000' # The TOKEN for your Discord bot
GUILD_ID = 0000  # Discord Server ID
CHANNEL_ID = 0000  # Target Channel ID for Message Sending
ROLE_NAME = 'ROLE' # Name of the Role to Mention

# Set the message sending time (hh:mm:ss.ff)
set_hour, set_minute, set_second, set_microsecond = 0, 0, 0, 0 # 00:00:00.00

# Set the check interval in seconds
# The default is to check every 60 seconds if it's time to send the message
interval = 60

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# Load date.json
def load_dates():
  try:
    with open('date.json', 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return {}


# Save date.json
def save_dates(dates):
  with open('date.json', 'w') as f:
    json.dump(dates, f)


# Get the target role
def get_target_role(guild):
  return discord.utils.get(guild.roles, name=ROLE_NAME)


# Set the timezone
set_time_zone = 'Asia/Taipei' # UTC+8
timezone = pytz.timezone(set_time_zone)


# Read the last notification date
def load_last_notification_date():
  try:
    with open('send.txt', 'r') as f:
      return f.read().strip()
  except FileNotFoundError:
    return None


# Update the last notification date
def update_last_notification_date(date):
  with open('send.txt', 'w') as f:
    f.write(date)


# Check the date before sending notification
async def check_notification_date(channel):
  last_date_str = load_last_notification_date()
  current_date = datetime.datetime.now(timezone).date()

  if last_date_str is None or last_date_str != current_date.strftime('%Y-%m-%d'):
    update_last_notification_date(current_date.strftime('%Y-%m-%d'))
    return True
  else:
    return False
  

# Send notification
async def check_reminders(channel, days_dict):
  now = datetime.datetime.now(timezone).date()
  target_role = get_target_role(channel.guild)
  notice_message = f'{target_role.mention}\n'
  for name, date_str in days_dict.items():
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    days_left = (date_obj - now).days
    if days_left == 0:
      notice_message += f"Today is {name}\n!"
    elif days_left > 0:
      notice_message += f'There are {days_left} days left until {name}!\n'
  await channel.send(notice_message)


@bot.event
async def on_ready():
  print('The bot has successfully logged in.')

  # Set the bot's status
  bot_status = "Game"
  activity = discord.Game(name=bot_status)
  await bot.change_presence(activity=activity)

  # Get the target server and channel
  guild = bot.get_guild(GUILD_ID)
  channel = guild.get_channel(CHANNEL_ID)

  # Read existing events
  days_dict = load_dates()

  while True:
    now = datetime.datetime.now(timezone)
    target_time = now.replace(hour=set_hour, minute=set_minute, second=set_second, microsecond=set_microsecond)

    if now >= target_time:
      # Check if today's countdown notification has not been sent yet
      should_send_notification = await check_notification_date(channel)
      if should_send_notification:
        # Send countdown notifications
        await check_reminders(channel, days_dict)
        pass

      # Calculate the next day's notification sending time
      next_target_time = target_time + datetime.timedelta(days=1)

      # Calculate the next time to check the current time
      sleep_seconds = (next_target_time - now).total_seconds()
      await asyncio.sleep(sleep_seconds)

    else:
      # Not yet at the specified notification time, continue waiting
      await asyncio.sleep(interval)


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  await bot.process_commands(message)


@bot.command()
async def test(ctx):
  test_message = "Alive"
  await ctx.send(test_message)


@bot.command()
async def add(ctx, date_str=None, name=None):
  if date_str is None or name is None:
    await ctx.send('Please provide the date and name of the event.')
    return

  try:
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    # Load existing events
    days_dict = load_dates()

    # Add an event
    days_dict[name] = str(date_obj)

    # Save date.json
    save_dates(days_dict)

    await ctx.send(f'Event has been added: {name} - {date_obj}')
  except ValueError:
    await ctx.send('Please use the correct date format (YYYY-MM-DD).')


@bot.command()
async def delete(ctx, name):
  # Load existing events
  days_dict = load_dates()

  if name in days_dict:
    # Delete an event
    del days_dict[name]

    # Save date.json
    save_dates(days_dict)

    await ctx.send(f'Event has been deleted: {name}')
  else:
    await ctx.send(f'Event named {name} cannot be found.')


@bot.command()
async def check(ctx):
  # Load existing events
  days_dict = load_dates()
  if days_dict:
    check_message = "The currently existing events are as follows:\n"
    for name, date_obj in days_dict.items():
      check_message += f"{name}: {date_obj}\n"
    await ctx.send(check_message)
  else:
    await ctx.send("Currently, there are no events.")


# Customize the bot's help command
class CustomHelpCommand(commands.DefaultHelpCommand):
  
  def get_command_signature(self, command):
    return f'{self.clean_prefix}{command.qualified_name} {command.signature}'
  
  @property
  def clean_prefix(self):
    return self.context.bot.command_prefix
  
  async def send_command_help(self, command):

    embed = discord.Embed(title='Command help',
                          description=command.help,
                          color=discord.Color.green())
    embed.add_field(name='Syntax',
                    value=self.get_command_signature(command),
                    inline=False)
    await self.get_destination().send(embed=embed)
    
  async def send_bot_help(self, mapping):
    all_command = {
      'help': '`!help command`\nInquire about the syntax of a specific command.\nexample:`!help add`',
      'test': "`!test`\nTest the bot's running status",
      'add':
      '`!add yyyy-mm-dd name`\nAdd an event named "name".\nexample:`!add 2023-01-01 Birthday`',
      'delete': '`!delete name`\nDelete the event named "name".\nexample:`!delete Birthday`',
      'check': '`!check`\nQuery the currently existing events.'
    }
    embed = discord.Embed(title='Tutorial',
                          description='Below are all the commands and usage tutorials for this Discord bot.',
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
