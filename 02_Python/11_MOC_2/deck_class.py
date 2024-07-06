import card_class
import random

class Deck:
    def __init__(self):
        self.all_cards = []

        for suit in card_class.suits:
            for rank in card_class.ranks:
                # Create the card Object
                created_card = card_class.Card(suit, rank)

                self.all_cards.append(created_card)

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

if __name__ == '__main__':
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
