import random

values = {'Ace':11, 'Two':2, 'Three':3, 'Four':4, 'Five':5,
            'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10,
            'Jack':10, 'Queen':10, 'King':10}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
            'Nine', 'Ten', 'Jack', 'Queen', 'King')

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self):
        self.all_cards = []
        for card_suit in suits:
            for card_rank in ranks:
                self.all_cards.append(Card(card_suit, card_rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

    def __str__(self):
        card_in_deck = ''
        for card in self.all_cards:
            card_in_deck += '\n' + card.__str__()
        return 'The deck has:' + card_in_deck

class Hand:

    def __init__(self):
        self.hand_value = 0
        self.current_hand = []
        self.aces_track = 0
    def add_card(self, card):
        self.current_hand.append(card)
        self.hand_value += values[card.rank]
        if card.rank == 'Ace':
            self.aces_track += 1
    def aces_adjuct(self):
        while self.hand_value > 21 and self.aces_track:
            self.hand_value -= 10
            self.aces_track -= 1
    def __str__(self):
        pass


class Chip:

    def __init__(self, pocket):
        self.pocket = pocket
        self.bet = 0

    def win(self):
        self.pocket += self.bet

    def lose(self):
        self.pocket -= self.bet

