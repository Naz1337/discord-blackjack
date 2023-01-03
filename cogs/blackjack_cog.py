from discord.ext import commands
from discord import app_commands, interactions
import discord
import logging
import aiosqlite

logger = logging.getLogger(__name__)


class BlackJack(commands.Cog):
    DB_FILENAME = 'blackjack.db'

    def __init__(self) -> None:
        super().__init__()

    async def cog_load(self):
        async with aiosqlite.connect(self.DB_FILENAME) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS player (
                    player_id INTEGER PRIMARY KEY,
                    balance REAL,
                    deposit REAL
                )
                """)

        logger.info("Loaded blackjack cog")

    @commands.command()
    @commands.is_owner()
    async def add_money(self, ctx: commands.Context, amount: float, to: discord.User = commands.Author):
        """add money to the person you choose without increasing deposit"""
        
        async with aiosqlite.connect(self.DB_FILENAME) as db:
            await db.execute(
                """
                    INSERT INTO player (player_id, balance, deposit)
                    VALUES (?, ?, ?)
                    ON CONFLICT (player_id) DO
                        UPDATE SET balance = balance + excluded.balance;
                """,
                (to.id, amount, 0))
            await db.commit()

            async with db.execute('SELECT balance, deposit FROM player WHERE player_id = ?', (to.id,)) as cur:
                async for row in cur:
                    balance, deposit = row

            resp = f"Added ${amount:,.2f} to {to}(${balance:,.2f}) without increasing their current deposit(${deposit:,.2f})"

            await ctx.send(resp, ephemeral=True)
            logger.info(resp)
    
    @app_commands.command()
    async def deposit(self, interaction: interactions.Interaction, amount: float):
        async with aiosqlite.connect(self.DB_FILENAME) as db:
            await db.execute(
                """
                INSERT INTO player (player_id, balance, deposit)
                VALUES (?, ?, ?)
                ON CONFLICT (player_id) DO UPDATE
                SET balance = balance + excluded.balance,
                    deposit = deposit + excluded.deposit;
                """,
                (interaction.user.id, amount, amount))
            await db.commit()

            async with db.execute('SELECT balance, deposit FROM player WHERE player_id = ?', (interaction.user.id,)) as cur:
                async for row in cur:
                    balance, deposit = row
            
            resp = f"Deposited ${amount:,.2f} to your balance(${balance:,.2f}). _Total Deposit: ${deposit:,.2f}_"
            await interaction.response.send_message(resp, ephemeral=True)
            logger.info(f"{resp} to {interaction.user}")


async def setup(bot: commands.Bot):
    blackjack_cog = BlackJack()
    await bot.add_cog(blackjack_cog)
