"""Deck module for Seven Poker.

Defines the Deck class for managing a standard 52-card deck.

Security Warning:
    This module uses Python's `random` module which is NOT cryptographically
    secure. For production online poker, use `secrets` module instead.

Thread Safety:
    Deck instances are NOT thread-safe. Each game session should use its own
    Deck instance. Do not share Deck objects across threads.
"""

import random
from collections.abc import Iterator

from .card import Card, Rank, Suit


class Deck:
    """A standard 52-card deck for Seven Poker.

    The deck can be shuffled and cards can be drawn from it.
    """

    def __init__(self, shuffle: bool = True) -> None:
        """Create a new deck with all 52 cards.

        Args:
            shuffle: If True, shuffle the deck after creation.
        """
        self._cards: list[Card] = self._create_full_deck()
        if shuffle:
            self.shuffle()

    @staticmethod
    def _create_full_deck() -> list[Card]:
        """Create a list of all 52 cards in a standard deck."""
        return [Card(suit, rank) for suit in Suit for rank in Rank]

    def shuffle(self) -> None:
        """Shuffle the deck in place using Fisher-Yates algorithm."""
        random.shuffle(self._cards)

    def draw(self) -> Card:
        """Draw and return the top card from the deck.

        Returns:
            The top card from the deck.

        Raises:
            IndexError: If the deck is empty.
        """
        if not self._cards:
            raise IndexError("Cannot draw from an empty deck")
        return self._cards.pop()

    def draw_many(self, count: int) -> list[Card]:
        """Draw multiple cards from the deck.

        Args:
            count: Number of cards to draw.

        Returns:
            List of drawn cards.

        Raises:
            ValueError: If count is negative.
            IndexError: If not enough cards remain.
        """
        if count < 0:
            raise ValueError("Count must be non-negative")
        if count > len(self._cards):
            raise IndexError(
                f"Cannot draw {count} cards, only {len(self._cards)} remaining"
            )
        drawn = self._cards[-count:]
        self._cards = self._cards[:-count]
        return list(reversed(drawn))

    def reset(self, shuffle: bool = True) -> None:
        """Reset the deck to a full 52-card deck.

        Args:
            shuffle: If True, shuffle after reset.
        """
        self._cards = self._create_full_deck()
        if shuffle:
            self.shuffle()

    @property
    def remaining(self) -> int:
        """Return the number of cards remaining in the deck."""
        return len(self._cards)

    def __len__(self) -> int:
        return len(self._cards)

    def __bool__(self) -> bool:
        return bool(self._cards)

    def __iter__(self) -> Iterator[Card]:
        """Iterate over remaining cards without removing them."""
        return iter(self._cards)

    def __repr__(self) -> str:
        return f"Deck(remaining={len(self._cards)})"

    def peek(self, count: int = 1) -> list[Card]:
        """Peek at the top cards without removing them.

        Args:
            count: Number of cards to peek at.

        Returns:
            List of cards from top of deck.

        Raises:
            ValueError: If count is negative or exceeds deck size.
        """
        if count < 0:
            raise ValueError("Count must be non-negative")
        if count > len(self._cards):
            raise ValueError(
                f"Cannot peek {count} cards, only {len(self._cards)} remaining"
            )
        return list(reversed(self._cards[-count:]))
