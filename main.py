import os
import logging

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv


@commands.hybrid_command()
async def ping(ctx: commands.Context):
    """Tell you the latency of this bot"""
    latency = int(ctx.bot.latency * 1000)
    await ctx.send(f"Pong {latency}ms", ephemeral=True)
    logging.info(
        f"{ctx.author} used ping and the current latency is {latency}ms")


@commands.hybrid_command()
@app_commands.describe(a='The first number', b='The second number')
async def add(ctx: commands.Context, a: int = commands.parameter(description='The first number'), b: int = commands.parameter(description='The second number')):
    """Add the two number that was given"""
    answer = f"{a} + {b} = {a + b} !"
    await ctx.send(answer, ephemeral=True)
    logging.info(f"{ctx.author} used add command: {answer}")


async def on_ready():
    global bot
    logging.info(
        f"Bot connected as {bot.user} (ID: {bot.user.id}), ready!")
    
    logging.debug('loading extension blackjack_cog')
    await bot.load_extension('cogs.blackjack_cog')
    
    logging.info("calling .sync on the bot tree")
    await bot.tree.sync()

@commands.hybrid_command()
@commands.is_owner()
async def reload(ctx: commands.Context, target_cog: str = 'cogs.blackjack_cog'):
    await bot.reload_extension(target_cog)
    resp = f"reloaded {target_cog}"
    logging.info(resp)
    await ctx.send(resp)

@reload.error
async def reload_error(ctx: commands.Context, exception: Exception):
    logging.error(f"Fail to reload whatever it was trying to reload, {exception}")
    if isinstance(exception, commands.ExtensionNotFound):
        await ctx.send("Extension does not exist")
    else:
        await ctx.send(f"Error! {exception}")


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    global bot  # from now own, this will be main.bot if someone import this and run main()
    bot = commands.Bot(
        'p!', description="The bot that handle your blackjack games", intents=intents)

    logger = logging.getLogger()  # root
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(
        '[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    file_handler = logging.FileHandler('logs.txt')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    load_dotenv()
    token = os.environ.get('dsc_key')

    bot.add_command(ping)
    bot.add_command(add)
    bot.add_command(reload)

    bot.add_listener(on_ready, 'on_ready')

    # run setup the console formatting logging stuff
    bot.run(token, log_level=logging.INFO, root_logger=True)


if __name__ == "__main__":
    main()
