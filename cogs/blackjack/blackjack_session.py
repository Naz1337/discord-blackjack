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
    # think of it like game state, we can have the
    # function for every option like hit and stand,
    # split and stuff, each function will check it
    # game state to see if the the valid move
    # and check who turn it is and update their hand
    # in the this class