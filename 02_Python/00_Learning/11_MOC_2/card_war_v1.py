import card_and_deck
import player_class

def print_a_deck(deck_list):
    for a_card in deck_list:
        print(a_card)

class GameStart:

    def __init__(self, player1, player2):
        # 1. Create a deck and shuffle
        self.game_deck = card_and_deck.Deck()
        self.game_deck.shuffle()
        # 2. Create 2 player
        self.player1 = player_class.Player(player1)
        self.player2 = player_class.Player(player2)
    def deal_all(self):
        player_index = 1
        for card in range(0, 52):
            top_card = self.game_deck.all_cards.pop()
            if player_index == 1:
                self.player1.add_cards(top_card)
                player_index = 2
            else:
                self.player2.add_cards(top_card)
                player_index = 1
    def game_over_check(self):
        if len(self.player1)
        pass

#===============================================================================
#===============================================================================
#===============================================================================

if __name__ == '__main__':
    # Init game here
    game = GameStart("Hans", "Laura")
    print(game.player1)
    print(game.player2)

    game.deal_all()
    print('\nAfter Deal')
    print(game.player1)
    print(game.player2)

    game_is_start = true

    while game_is_start:
