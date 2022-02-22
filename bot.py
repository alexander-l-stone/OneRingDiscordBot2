from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = getenv("TOKEN")

bot = commands.Bot(command_prefix="!")

@bot.command(name="hello")
async def hello_world(ctx: commands.Context):
    await ctx.send("Hello, World!")

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

bot.run(token)