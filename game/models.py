# Donsol game
import random
from time import time

class Card:

    def __init__(self, suit, value, name=None):
        self.suit = suit
        self.name = name or suit
        self.value = value

    def is_monster(self):
        return self.suit in ['spade', 'club']


class Player:

    def __init__(self):
        self.max_health = 21
        self.health = self.max_health
        self.shield = None
        self.can_drink_potion = True
        self.escaped_last_room = False

    def handle_monster(self, monster_value):
        damage = monster_value
        if self.shield:
            broken, damage = self.shield.handle_monster(monster_value)
            if broken:
                self.shield = None
        self.health = max(0, self.health - damage)


class Shield:

    def __init__(self, value):
        self.value = value
        self.previous_value = None

    def handle_monster(self, monster_value):
        """Return tuple of broken boolean and damage taken"""
        broken = False
        if self.previous_value is not None and monster_value >= self.previous_value:
            # logging.getLogger('history', 'Shield Broke!')A
            broken = True
            self.value = 0
        self.previous_value = monster_value
        return (broken, max(0, monster_value - self.value))


class Room:

    def __init__(self, cards, player_escaped_previous_room=False):
        self.slots = dict(zip('jkl;', cards))
        self.player_escaped_previous_room = player_escaped_previous_room

    def flee(self):
        """
        Fleeing returns None if unable to flee, else returns the set of
        cards to return to the deck
        """
        if self.escapable():
            return self.slots.values()
        return None

    def select_card(self, key):
        """
        Return the card at 'key' from the room, and remove it from the rooms'
        storage. If given an invalid key, return None
        """
        try:
            return self.slots.pop(key)
        except KeyError:
            return None

    def escapable(self):
        """Check whether or not the room is escapable"""
        if self.player_escaped_previous_room:
            monsters_remain = any(c.is_monster() for c in self.slots.values())
            if monsters_remain:
                return False
        return True


class Deck:
    """A deck holds an ordered set of cards and can pop or shuffle them"""

    def __init__(self, cards, seed=None):
        """Optionally accept a seed to make the deck deterministic"""
        self.cards = cards
        self.random = random.Random()
        if seed is None:
            seed = time()

        self.random.seed(seed)
        print("Deck's random seed is: {}".format(seed))

    def draw(self, count):
        """
        Draw <count> cards from the deck, or as many as are available.
        return a list of cards drawn.
        """
        drawn = []
        while len(drawn) < count:
            try:
                drawn.append(self.cards.pop())
            except IndexError:
                break
        return drawn

    def shuffle(self):
        self.random.shuffle(self.cards)

    def add(self, cards):
        """Add the passed list of cards to the deck"""
        self.cards.extend(cards)


# Build Deck
# x2, clubs and spades
heartCards = [
    {'value': 2, 'name': ''},
    {'value': 3, 'name': ''},
    {'value': 4, 'name': ''},
    {'value': 5, 'name': ''},
    {'value': 6, 'name': ''},
    {'value': 7, 'name': ''},
    {'value': 8, 'name': ''},
    {'value': 9, 'name': ''},
    {'value': 10, 'name': ''},
    {'value': 11, 'name': ''},
    {'value': 11, 'name': ''},
    {'value': 11, 'name': ''},
    {'value': 11, 'name': ''},
]

diamondCards = [
    {'value': 2, 'name': ''},
    {'value': 3, 'name': ''},
    {'value': 4, 'name': ''},
    {'value': 5, 'name': ''},
    {'value': 6, 'name': ''},
    {'value': 7, 'name': ''},
    {'value': 8, 'name': ''},
    {'value': 9, 'name': ''},
    {'value': 10, 'name': ''},
    {'value': 11, 'name': ''},
    {'value': 11, 'name': ''},
    {'value': 11, 'name': ''},
    {'value': 11, 'name': ''},
]

clubCards = [
    {'value': 2, 'name': ''},
    {'value': 3, 'name': ''},
    {'value': 4, 'name': ''},
    {'value': 5, 'name': ''},
    {'value': 6, 'name': ''},
    {'value': 7, 'name': ''},
    {'value': 8, 'name': ''},
    {'value': 9, 'name': ''},
    {'value': 10, 'name': ''},
    {'value': 11, 'name': ''},
    {'value': 13, 'name': ''},
    {'value': 15, 'name': ''},
    {'value': 17, 'name': ''},
]

spadeCards = [
    {'value': 2, 'name': ''},
    {'value': 3, 'name': ''},
    {'value': 4, 'name': ''},
    {'value': 5, 'name': ''},
    {'value': 6, 'name': ''},
    {'value': 7, 'name': ''},
    {'value': 8, 'name': ''},
    {'value': 9, 'name': ''},
    {'value': 10, 'name': ''},
    {'value': 11, 'name': ''},
    {'value': 13, 'name': ''},
    {'value': 15, 'name': ''},
    {'value': 17, 'name': ''},
]

DECK = []

hearts = [Card('potion', cardInfo['value'], name = cardInfo['name']) for cardInfo in heartCards]
diamonds = [Card('shield', cardInfo['value'], name = cardInfo['name']) for cardInfo in diamondCards]
clubs = [Card('monster', cardInfo['value'], name = cardInfo['name']) for cardInfo in clubCards]
spades = [Card('monster', cardInfo['value'], name = cardInfo['name']) for cardInfo in spadeCards]
jokers = [Card('monster', 21, name='Donsol'), Card('monster', 21, name = 'Donsol')]

DECK = [card for suit in [hearts, diamonds, clubs, spades, jokers] for card in suit]

PLAYER = Player()
