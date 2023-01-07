from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Set

import discord

from .card import Card
from .deck import Deck


class BetBelowMinimum(Exception):
    ...


class NotAppropriatePhase(Exception):
    ...


class NotYourTurn(Exception):
    ...


class BlackJackPhase(Enum):
    BETANDJOIN = auto()
    DRAWING = auto()
    PLAYERCHOOSE = auto()
    POST = auto()


@dataclass(slots=True)
class PlayerHand:
    player: discord.Member
    bet_amount: float
    hand: List[Card] = field(default_factory=list)

    @property
    def hand_total(self):
        return sum([card.value for card in self.hand])


@dataclass(slots=True)
class BlackJackSession:
    """
    class that hold Black Jack session.

    Attributes
    ----------
    playing_players: List[discord.Member]
        players in here shouuld be not busted yet
    """
    channel_id: int
    deck: Deck = field(default=None)
    game_phase: BlackJackPhase = field(default=BlackJackPhase.BETANDJOIN)
    dealer_hand: List[Card] = field(default_factory=list)
    players_hand: List[PlayerHand] = field(default_factory=dict)
    current_hand: PlayerHand = field(default=None)
    players_hand_final: List[PlayerHand] = field(default_factory=list)
    minimum_bet: float = 25

    def __post_init__(self):
        self.deck = Deck(2, True)

    def bet(self, player: discord.Member, bet_amount: float):
        if bet_amount < self.minimum_bet:
            raise BetBelowMinimum("You has betted below mininum.")
        
        if self.game_phase != BlackJackPhase.BETANDJOIN:
            raise NotAppropriatePhase("You cannot bet now.")

        player_hand = PlayerHand(player, bet_amount)
        self.players_hand.append(player_hand)

    def start_dealing(self):
        if self.game_phase != BlackJackPhase.BETANDJOIN:
            raise NotAppropriatePhase(f"Wow, this function should not be called right now {self.game_phase}")
        self.game_phase = BlackJackPhase.DRAWING

        self.players_hand.reverse()

        for player_hand in self.players_hand:
            player_hand.hand.append(self.deck.take_card())

        self.dealer_hand.append(self.deck.take_card())
        
        for player_hand in self.players_hand:
            player_hand.hand.append(self.deck.take_card())
        
        self.dealer_hand.append(self.deck.take_card())
        
        self.current_hand = self.players_hand.pop()

        self.game_phase = BlackJackPhase.PLAYERCHOOSE
    
    def hit(self, player: discord.Member):
        if self.current_hand.player != player:
            raise NotYourTurn("Not your turn.")
        
        self.current_hand.hand.append(self.deck.take_card())

        current_hand_total = self.current_hand.hand_total

        if current_hand_total > 20:
            # if hand total is more than 20
            # which is 21(blackjack!) or bust
            self.players_hand_final.append(self.current_hand)
            self.current_hand = self.players_hand.pop()
        
        return current_hand_total

    # add attribute for players card, players turn
    # should this place run the discord bot?
    # think of it like game state, we can have the
    # function for every option like hit and stand,
    # split and stuff, each function will check it
    # game state to see if the the valid move
    # and check who turn it is and update their hand
    # in the this class

    # DRAWING phase text
    # during DRAWING phase, just do the drawing
    # using python then just what we end up with
    """
    Dealer's hand:
    10 + ? = 10

    Player 1:
    8 + 8 = 16

    Player 2:
    A + 10 = 21

    Player 3:
    2 + 10 = 12
    """
