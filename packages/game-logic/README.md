# Seven Poker Game Logic

Pure Python implementation of Korean Seven Poker game logic.

## Installation

```bash
cd packages/game-logic
pip install -e ".[dev]"
```

## Usage

### Card and Deck

```python
from game_logic import Card, Deck, Suit, Rank

# Create a card
ace_of_spades = Card(Suit.SPADE, Rank.ACE)
print(ace_of_spades)  # A♠

# Create from string notation
card = Card.from_string("KH")  # King of Hearts
print(card)  # K♥

# Create and shuffle a deck
deck = Deck()
print(f"Cards remaining: {deck.remaining}")  # 52

# Draw cards
card = deck.draw()
hand = deck.draw_many(4)

# Peek without removing
top_cards = deck.peek(3)

# Reset deck
deck.reset()
```

### Suit Rankings (Korean Seven Poker)

Suits are ranked for tiebreakers:
- Spade (♠) > Diamond (♦) > Heart (♥) > Club (♣)

```python
from game_logic import Suit

# Compare suits
assert Suit.SPADE > Suit.DIAMOND > Suit.HEART > Suit.CLUB

# Get Korean names
print(Suit.SPADE.name_ko)  # 스페이드
```

### Card Comparison

Cards compare by rank first, then by suit:

```python
from game_logic import Card, Suit, Rank

ace_spade = Card(Suit.SPADE, Rank.ACE)
ace_heart = Card(Suit.HEART, Rank.ACE)
king_spade = Card(Suit.SPADE, Rank.KING)

# Ace beats King
assert ace_heart > king_spade

# Same rank: Spade beats Heart
assert ace_spade > ace_heart
```

## Testing

```bash
pytest
pytest --cov=game_logic
```

## API Reference

### `Suit` (Enum)

Card suits with Korean Seven Poker ranking.

| Value | Symbol | Korean |
|-------|--------|--------|
| SPADE | ♠ | 스페이드 |
| DIAMOND | ♦ | 다이아몬드 |
| HEART | ♥ | 하트 |
| CLUB | ♣ | 클로버 |

### `Rank` (Enum)

Card ranks from TWO (2) to ACE (14).

### `Card`

- `Card(suit: Suit, rank: Rank)` - Create a card
- `Card.from_string(s: str)` - Parse from string (e.g., "AS", "10H")
- `card.suit` - Get suit
- `card.rank` - Get rank
- Supports comparison (`<`, `>`, `==`) and hashing

### `Deck`

- `Deck(shuffle: bool = True)` - Create 52-card deck
- `deck.draw()` - Draw one card
- `deck.draw_many(n)` - Draw n cards
- `deck.peek(n)` - Look at top n cards
- `deck.shuffle()` - Shuffle deck
- `deck.reset()` - Reset to full deck
- `deck.remaining` - Cards left
- `len(deck)` - Cards left
- `bool(deck)` - True if cards remain
