from dataclasses import dataclass, field
from .suit import Suit


@dataclass(slots=False, frozen=True)
class Card:
    suit: Suit = field(compare=False)
    value: int  # possible values are
                # 2, 3, 4, 5, 6, 7, 8
                # 9, 10, 10(For jack),
                # 10(for queen),
                # 10(for king),
                # 11(for aces)

    def __post_init__(self):
        if self.value < 1 or \
           self.value > 11:  # < 1 because 11(ace) can turn to 1
            raise ValueError("Value for card is out of logical range")
