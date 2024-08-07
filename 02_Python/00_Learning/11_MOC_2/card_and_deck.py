# This is all ==================================================================
import random

values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6,
            'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10,
            'Jack':11, 'Queen':12, 'King':13, 'Ace':14}
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
            'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
suits_indent = 2
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                # Create the card Object
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

#===============================================================================
#===============================================================================
#===============================================================================

if __name__ == '__main__':

    print('{:*^50}'.format('Card Class Check'))
    #Create a card
    two_hearts = Card(suits[0], ranks[2 - suits_indent])
    #Print a card
    print(two_hearts)
    print('{:*^50}\n'.format(''))

    print('{:*^50}'.format('Deck Class Check'))
    # Create a deck, with card from Card class
    new_deck = Deck()
    # Create a shuffle deck
    new_deck.shuffle()
    # Print all Card in Deck
    for card_obj in new_deck.all_cards:
        print(card_obj)
    # Get a card
    my_card = new_deck.deal_one()
    print('\n{:=^30}'.format('| GET A CARD |'))
    print('>>>>> You got: ')
    print(my_card)
    print('{:=^30}'.format("| REMAIN " + str(len(new_deck.all_cards)) + " |"))
    print('{:*^50}\n'.format(''))
