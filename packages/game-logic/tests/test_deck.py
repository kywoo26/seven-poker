"""Tests for Deck class."""

import pytest

from game_logic import Card, Deck, Rank, Suit


class TestDeck:
    """Tests for Deck class."""

    def test_deck_creation(self) -> None:
        """New deck should have 52 cards."""
        deck = Deck(shuffle=False)
        assert len(deck) == 52
        assert deck.remaining == 52

    def test_deck_contains_all_cards(self) -> None:
        """Deck should contain all 52 unique cards."""
        deck = Deck(shuffle=False)
        cards = list(deck)
        assert len(cards) == 52
        assert len(set(cards)) == 52

        for suit in Suit:
            for rank in Rank:
                assert Card(suit, rank) in cards

    def test_deck_draw(self) -> None:
        """Drawing should remove and return top card."""
        deck = Deck(shuffle=False)
        initial_count = len(deck)

        card = deck.draw()

        assert isinstance(card, Card)
        assert len(deck) == initial_count - 1

    def test_deck_draw_empty(self) -> None:
        """Drawing from empty deck should raise IndexError."""
        deck = Deck(shuffle=False)
        for _ in range(52):
            deck.draw()

        with pytest.raises(IndexError, match="empty deck"):
            deck.draw()

    def test_deck_draw_many(self) -> None:
        """Drawing multiple cards should work correctly."""
        deck = Deck(shuffle=False)
        cards = deck.draw_many(5)

        assert len(cards) == 5
        assert len(deck) == 47
        assert all(isinstance(c, Card) for c in cards)

    def test_deck_draw_many_too_many(self) -> None:
        """Drawing more cards than available should raise IndexError."""
        deck = Deck(shuffle=False)
        deck.draw_many(50)

        with pytest.raises(IndexError, match="Cannot draw 5 cards"):
            deck.draw_many(5)

    def test_deck_draw_many_negative(self) -> None:
        """Drawing negative cards should raise ValueError."""
        deck = Deck(shuffle=False)

        with pytest.raises(ValueError, match="non-negative"):
            deck.draw_many(-1)

    def test_deck_shuffle(self) -> None:
        """Shuffling should randomize card order."""
        deck1 = Deck(shuffle=False)
        deck2 = Deck(shuffle=False)

        cards1_before = list(deck1)
        deck1.shuffle()
        cards1_after = list(deck1)

        cards2 = list(deck2)

        assert cards1_before == cards2
        assert len(cards1_after) == 52
        assert set(cards1_after) == set(cards1_before)

    def test_deck_shuffle_randomness(self) -> None:
        """Multiple shuffles should produce different orders (with high probability)."""
        orders = []
        for _ in range(10):
            deck = Deck(shuffle=True)
            orders.append(tuple(deck))

        unique_orders = set(orders)
        assert len(unique_orders) > 1

    def test_deck_reset(self) -> None:
        """Reset should restore deck to full 52 cards."""
        deck = Deck(shuffle=False)
        deck.draw_many(20)
        assert len(deck) == 32

        deck.reset(shuffle=False)
        assert len(deck) == 52

    def test_deck_bool(self) -> None:
        """Deck should be truthy when cards remain, falsy when empty."""
        deck = Deck(shuffle=False)
        assert bool(deck) is True

        for _ in range(52):
            deck.draw()

        assert bool(deck) is False

    def test_deck_peek(self) -> None:
        """Peek should show top cards without removing them."""
        deck = Deck(shuffle=False)

        peeked = deck.peek(3)
        assert len(peeked) == 3
        assert len(deck) == 52

        drawn = deck.draw_many(3)
        assert peeked == drawn

    def test_deck_peek_invalid(self) -> None:
        """Peek with invalid count should raise ValueError."""
        deck = Deck(shuffle=False)

        with pytest.raises(ValueError, match="non-negative"):
            deck.peek(-1)

        with pytest.raises(ValueError, match="Cannot peek"):
            deck.peek(100)

    def test_deck_repr(self) -> None:
        """Deck should have informative repr."""
        deck = Deck(shuffle=False)
        assert repr(deck) == "Deck(remaining=52)"

        deck.draw_many(10)
        assert repr(deck) == "Deck(remaining=42)"

    def test_deck_iteration(self) -> None:
        """Iterating deck should not remove cards."""
        deck = Deck(shuffle=False)

        count = sum(1 for _ in deck)
        assert count == 52
        assert len(deck) == 52


class TestDeckIntegration:
    """Integration tests for Deck with Card."""

    def test_deal_to_players(self) -> None:
        """Simulate dealing 4 cards to 5 players."""
        deck = Deck()
        players = [[] for _ in range(5)]

        for _ in range(4):
            for player_hand in players:
                player_hand.append(deck.draw())

        for hand in players:
            assert len(hand) == 4

        assert len(deck) == 52 - 20

    def test_seven_poker_deal_simulation(self) -> None:
        """Simulate Seven Poker initial deal (4 cards per player, 1 discarded)."""
        deck = Deck()
        num_players = 5

        initial_hands = [deck.draw_many(4) for _ in range(num_players)]

        kept_hands = [hand[:3] for hand in initial_hands]

        for hand in kept_hands:
            assert len(hand) == 3

        assert len(deck) == 52 - 20
