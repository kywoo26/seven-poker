"""Tests for Card, Suit, and Rank classes."""

import pytest

from game_logic import Card, Rank, Suit


class TestSuit:
    """Tests for Suit enum."""

    def test_suit_ordering(self) -> None:
        """Suits should be ordered: Club < Heart < Diamond < Spade."""
        assert Suit.CLUB < Suit.HEART < Suit.DIAMOND < Suit.SPADE

    def test_suit_values(self) -> None:
        """Suit values should reflect ranking."""
        assert Suit.CLUB.value == 1
        assert Suit.HEART.value == 2
        assert Suit.DIAMOND.value == 3
        assert Suit.SPADE.value == 4

    def test_suit_symbols(self) -> None:
        """Suits should have correct Unicode symbols."""
        assert str(Suit.SPADE) == "\u2660"
        assert str(Suit.DIAMOND) == "\u2666"
        assert str(Suit.HEART) == "\u2665"
        assert str(Suit.CLUB) == "\u2663"

    def test_suit_korean_names(self) -> None:
        """Suits should have correct Korean names."""
        assert Suit.SPADE.name_ko == "\uc2a4\ud398\uc774\ub4dc"
        assert Suit.DIAMOND.name_ko == "\ub2e4\uc774\uc544\ubab0\ub4dc"
        assert Suit.HEART.name_ko == "\ud558\ud2b8"
        assert Suit.CLUB.name_ko == "\ud074\ub85c\ubc84"


class TestRank:
    """Tests for Rank enum."""

    def test_rank_ordering(self) -> None:
        """Ranks should be ordered from 2 to Ace."""
        assert Rank.TWO < Rank.THREE < Rank.TEN < Rank.JACK < Rank.QUEEN < Rank.KING < Rank.ACE

    def test_rank_values(self) -> None:
        """Rank values should be numeric."""
        assert Rank.TWO.value == 2
        assert Rank.TEN.value == 10
        assert Rank.JACK.value == 11
        assert Rank.QUEEN.value == 12
        assert Rank.KING.value == 13
        assert Rank.ACE.value == 14

    def test_rank_string(self) -> None:
        """Ranks should have correct string representation."""
        assert str(Rank.TWO) == "2"
        assert str(Rank.TEN) == "10"
        assert str(Rank.JACK) == "J"
        assert str(Rank.QUEEN) == "Q"
        assert str(Rank.KING) == "K"
        assert str(Rank.ACE) == "A"


class TestCard:
    """Tests for Card class."""

    def test_card_creation(self) -> None:
        """Cards should be created with suit and rank."""
        card = Card(Suit.SPADE, Rank.ACE)
        assert card.suit == Suit.SPADE
        assert card.rank == Rank.ACE

    def test_card_string(self) -> None:
        """Cards should have correct string representation."""
        assert str(Card(Suit.SPADE, Rank.ACE)) == "A\u2660"
        assert str(Card(Suit.HEART, Rank.TEN)) == "10\u2665"
        assert str(Card(Suit.DIAMOND, Rank.KING)) == "K\u2666"
        assert str(Card(Suit.CLUB, Rank.TWO)) == "2\u2663"

    def test_card_repr(self) -> None:
        """Cards should have informative repr."""
        card = Card(Suit.SPADE, Rank.ACE)
        assert repr(card) == "Card(SPADE, ACE)"

    def test_card_equality(self) -> None:
        """Cards with same suit and rank should be equal."""
        card1 = Card(Suit.SPADE, Rank.ACE)
        card2 = Card(Suit.SPADE, Rank.ACE)
        card3 = Card(Suit.HEART, Rank.ACE)

        assert card1 == card2
        assert card1 != card3

    def test_card_comparison_by_rank(self) -> None:
        """Cards should compare by rank first."""
        ace_club = Card(Suit.CLUB, Rank.ACE)
        king_spade = Card(Suit.SPADE, Rank.KING)

        assert king_spade < ace_club

    def test_card_comparison_by_suit(self) -> None:
        """Cards with same rank should compare by suit."""
        ace_spade = Card(Suit.SPADE, Rank.ACE)
        ace_heart = Card(Suit.HEART, Rank.ACE)
        ace_diamond = Card(Suit.DIAMOND, Rank.ACE)
        ace_club = Card(Suit.CLUB, Rank.ACE)

        assert ace_club < ace_heart < ace_diamond < ace_spade

    def test_card_hash(self) -> None:
        """Cards should be hashable for use in sets/dicts."""
        card1 = Card(Suit.SPADE, Rank.ACE)
        card2 = Card(Suit.SPADE, Rank.ACE)
        card3 = Card(Suit.HEART, Rank.ACE)

        assert hash(card1) == hash(card2)
        assert hash(card1) != hash(card3)

        card_set = {card1, card2, card3}
        assert len(card_set) == 2

    def test_card_from_string(self) -> None:
        """Cards should be creatable from string notation."""
        assert Card.from_string("AS") == Card(Suit.SPADE, Rank.ACE)
        assert Card.from_string("10H") == Card(Suit.HEART, Rank.TEN)
        assert Card.from_string("KD") == Card(Suit.DIAMOND, Rank.KING)
        assert Card.from_string("2c") == Card(Suit.CLUB, Rank.TWO)

    def test_card_from_string_invalid_suit(self) -> None:
        """Invalid suit should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid suit"):
            Card.from_string("AX")

    def test_card_from_string_invalid_rank(self) -> None:
        """Invalid rank should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rank"):
            Card.from_string("1S")

    def test_card_from_string_too_short(self) -> None:
        """Too short string should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid card string"):
            Card.from_string("A")

    def test_card_sorting(self) -> None:
        """Cards should sort correctly."""
        cards = [
            Card(Suit.CLUB, Rank.ACE),
            Card(Suit.SPADE, Rank.TWO),
            Card(Suit.SPADE, Rank.ACE),
            Card(Suit.HEART, Rank.ACE),
        ]
        sorted_cards = sorted(cards)

        assert sorted_cards[0] == Card(Suit.SPADE, Rank.TWO)
        assert sorted_cards[1] == Card(Suit.CLUB, Rank.ACE)
        assert sorted_cards[2] == Card(Suit.HEART, Rank.ACE)
        assert sorted_cards[3] == Card(Suit.SPADE, Rank.ACE)
