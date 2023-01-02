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


def main():
    intents = discord.Intents.default()
    intents.message_content = True
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

    async def on_ready():
        logging.info(
            f"Bot connected as {bot.user} (ID: {bot.user.id}), ready!")
        logging.info("calling .sync on the bot tree")
        await bot.tree.sync()

    bot.add_listener(on_ready, 'on_ready')

    # run setup the console formatting logging stuff
    bot.run(token, log_level=logging.INFO, root_logger=True)


if __name__ == "__main__":
    main()
