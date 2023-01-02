import os
import logging

import discord
from discord import app_commands
from dotenv import load_dotenv


@app_commands.command()
async def ping(interaction: discord.Interaction):
    """Tell you the latency of this bot"""
    await interaction.response.send_message(f"Pong {int(interaction.client.latency * 1000)}ms!", ephemeral=True)


class MyClient(discord.Client):
    MY_GUILD = discord.Object(id=347361743585935361)
    def __init__(self, intents: discord.Intents) -> None:
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=self.MY_GUILD)
        await self.tree.sync(guild=self.MY_GUILD)
    
    async def on_ready(self):
        logging.info(f"Logged in as {self.user} (ID: {self.user.id}), bot is ready!")
    
    

if __name__ == "__main__":
    load_dotenv()

    logger = logging.getLogger()
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    file_handler = logging.FileHandler('logs.txt')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    token: str = os.environ.get('dsc_key')
    client = MyClient(discord.Intents.default())
    client.tree.add_command(ping)
    client.run(token, root_logger=True)
