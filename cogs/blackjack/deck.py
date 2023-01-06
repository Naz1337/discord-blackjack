from typing import List, Optional
import random
from .card import Card
from .suit import Suit


class Deck:
    def __init__(self, fill_deck: Optional[int] = None, shuffle: bool = False):
        self.cards: List[Card] = []

        if fill_deck is not None:
            self.add_cards(fill_deck)
        
        if shuffle:
            self.shuffle_card()
    
    def add_cards(self, number_of_deck = 1):
        """
        add 52 card per deck
        """
        if number_of_deck <= 0:
            return
        suits: List[Suit] = list(Suit.__members__.values())
        for _ in range(number_of_deck):
            for suit in suits:
                for number in range(2, 11):  # does not include 11
                    self.cards.append(Card(suit, number))
                
                # add for jack, queen and king
                for _ in range(3):
                    self.cards.append(Card(suit, 10))
                
                #ace!
                self.cards.append(Card(suit, 11))
    
    def shuffle_card(self):
        random.shuffle(self.cards)
