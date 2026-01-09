"""Card module for Seven Poker.

Defines Suit, Rank enums and Card class representing a playing card.
"""

from enum import IntEnum
from functools import total_ordering


class Suit(IntEnum):
    """Card suits with Korean Seven Poker ranking.

    Ranking (high to low): Spade > Diamond > Heart > Club
    """

    CLUB = 1
    HEART = 2
    DIAMOND = 3
    SPADE = 4

    def __str__(self) -> str:
        symbols = {
            Suit.SPADE: "\u2660",
            Suit.DIAMOND: "\u2666",
            Suit.HEART: "\u2665",
            Suit.CLUB: "\u2663",
        }
        return symbols[self]

    @property
    def symbol(self) -> str:
        """Return the Unicode symbol for this suit."""
        return str(self)

    @property
    def name_ko(self) -> str:
        """Return the Korean name for this suit."""
        names = {
            Suit.SPADE: "\uc2a4\ud398\uc774\ub4dc",
            Suit.DIAMOND: "\ub2e4\uc774\uc544\ubab0\ub4dc",
            Suit.HEART: "\ud558\ud2b8",
            Suit.CLUB: "\ud074\ub85c\ubc84",
        }
        return names[self]


class Rank(IntEnum):
    """Card ranks from 2 to Ace.

    Ace is highest (14) for normal comparisons.
    For straights, Ace can also be low (handled in hand evaluation).
    """

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self) -> str:
        if self.value <= 10:
            return str(self.value)
        return {Rank.JACK: "J", Rank.QUEEN: "Q", Rank.KING: "K", Rank.ACE: "A"}[self]

    @property
    def symbol(self) -> str:
        """Return the display symbol for this rank."""
        return str(self)


@total_ordering
class Card:
    """A playing card with suit and rank.

    Cards are compared first by rank, then by suit (for tiebreakers).
    """

    __slots__ = ("_suit", "_rank")

    def __init__(self, suit: Suit, rank: Rank) -> None:
        """Create a new card.

        Args:
            suit: The card's suit.
            rank: The card's rank.
        """
        self._suit = suit
        self._rank = rank

    @property
    def suit(self) -> Suit:
        """Return the card's suit."""
        return self._suit

    @property
    def rank(self) -> Rank:
        """Return the card's rank."""
        return self._rank

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self._suit == other._suit and self._rank == other._rank

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        if self._rank != other._rank:
            return self._rank < other._rank
        return self._suit < other._suit

    def __hash__(self) -> int:
        return hash((self._suit, self._rank))

    def __repr__(self) -> str:
        return f"Card({self._suit.name}, {self._rank.name})"

    def __str__(self) -> str:
        return f"{self._rank}{self._suit}"

    @classmethod
    def from_string(cls, card_str: str) -> "Card":
        """Create a card from a string like 'AS' (Ace of Spades) or '10H' (10 of Hearts).

        Args:
            card_str: String representation (rank + suit initial).
                     Suit initials: S=Spade, D=Diamond, H=Heart, C=Club
                     Rank: 2-10, J, Q, K, A

        Returns:
            A new Card instance.

        Raises:
            ValueError: If the string format is invalid.
        """
        card_str = card_str.upper().strip()
        if len(card_str) < 2:
            raise ValueError(f"Invalid card string: {card_str}")

        suit_char = card_str[-1]
        rank_str = card_str[:-1]

        suit_map = {"S": Suit.SPADE, "D": Suit.DIAMOND, "H": Suit.HEART, "C": Suit.CLUB}
        if suit_char not in suit_map:
            raise ValueError(f"Invalid suit: {suit_char}")
        suit = suit_map[suit_char]

        rank_map = {
            "2": Rank.TWO,
            "3": Rank.THREE,
            "4": Rank.FOUR,
            "5": Rank.FIVE,
            "6": Rank.SIX,
            "7": Rank.SEVEN,
            "8": Rank.EIGHT,
            "9": Rank.NINE,
            "10": Rank.TEN,
            "J": Rank.JACK,
            "Q": Rank.QUEEN,
            "K": Rank.KING,
            "A": Rank.ACE,
        }
        if rank_str not in rank_map:
            raise ValueError(f"Invalid rank: {rank_str}")
        rank = rank_map[rank_str]

        return cls(suit, rank)
