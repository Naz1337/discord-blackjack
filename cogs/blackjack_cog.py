from discord.ext import commands
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
                    cash REAL
                )
                """)

        logger.info("Loaded blackjack cog")

    @commands.command()
    @commands.is_owner()
    async def add_money(self, ctx: commands.Context, amount: int, to: discord.User = commands.Author):
        """add money to the person you choose"""
        
        
        async with aiosqlite.connect(self.DB_FILENAME) as db:
            await db.execute(
                """
                    INSERT OR REPLACE INTO player (player_id, cash)
                    VALUES (?, ?)
                    ON CONFLICT (player_id) DO
                        UPDATE SET cash = cash + excluded.cash;
                """,
                (to.id, amount))
            await db.commit()

            async with db.execute('SELECT * FROM player WHERE player_id = ?', (to.id,)) as cur:
                async for row in cur:
                    cash = row[1]  # cash sit at the second column

            resp = f"Added ${amount} to {to}(${cash})"

            await ctx.send(resp)
            logger.info(resp)


async def setup(bot: commands.Bot):
    blackjack_cog = BlackJack()
    await bot.add_cog(blackjack_cog)
