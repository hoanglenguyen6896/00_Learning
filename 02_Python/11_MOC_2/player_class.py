# This is all ==================================================================
class Player:

    def __init__(self, name):
        self.name = name
        self.all_cards = []

    def remove_one(self):
        return self.all_cards.pop()

    def add_cards(self, new_cards):
        if type(new_cards) == type([]):
            # Add multiple cards
            self.all_cards.extend(new_cards)
        else:
            # Add a single card
            self.all_cards.append(new_cards)

    def __str__(self):
        return f'Player {self.name} has {len(self.all_cards)} cards'

#===============================================================================
#===============================================================================
#===============================================================================

if __name__ == '__main__':
    import card_and_deck

    new_player = Player("Hoang")
    print(new_player)

    new_cards = card_and_deck.Card(card_and_deck.suits[3],
                    card_and_deck.ranks[14 - card_and_deck.suits_indent])
    print("Create a new Card")
    print(new_cards)
    new_player.add_cards(new_cards)
    new_player.add_cards(new_cards)
    new_player.add_cards(new_cards)

    print(f"Player {new_player.name} current cards")
    print(new_player)

    new_player.remove_one()
    print(new_player)
