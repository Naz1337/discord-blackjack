from dataclasses import dataclass, field
from typing import List
import discord

from .deck import Deck

@dataclass
class BlackJackSession:
    id: int
    channel_id: int
    deck: Deck

    players: List[discord.Member] = field(default_factory=list)

    # add attribute for players card, players turn
    # should this place run the discord bot?