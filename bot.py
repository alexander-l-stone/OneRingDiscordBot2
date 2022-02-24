from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("TOKEN")

bot = commands.Bot(command_prefix="/")

bot.load_extension('one_ring')

bot.run(token)