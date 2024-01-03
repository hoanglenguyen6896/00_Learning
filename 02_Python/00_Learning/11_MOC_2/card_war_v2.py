import card_and_deck
import player_class

number_card_for_war = 10
game_on = True
round_number = 0


player_one = player_class.Player("Hans")
player_two = player_class.Player("Laura")


new_deck = card_and_deck.Deck()
new_deck.shuffle()

for card in range(0,26):
    player_one.add_cards(new_deck.deal_one())
    player_two.add_cards(new_deck.deal_one())
    # print(player_one.all_cards[-1])
    # print(player_two.all_cards[-1])


while game_on:
    round_number += 1
    print(f'Round {round_number}')

    # Check winning basic
    if(len(player_one.all_cards) == 0):
        print(f'Player {player_one.name} out of cards!' +
            f'\nPlayer {player_two.name} has won!!!')
        game_on = False
        break
    elif(len(player_two.all_cards) == 0):
        print(f'Player {player_two.name} out of cards!' +
            f'\nPlayer {player_one.name} has won!!!')
        game_on = False
        break

    # Start a new round
    player_one_cards = []
    player_one_cards.append(player_one.remove_one())

    player_two_cards = []
    player_two_cards.append(player_two.remove_one())

    # We use war to check card

    war_occur = True

    while war_occur:

        if player_one_cards[-1].value > player_two_cards[-1].value:
            player_one.add_cards(player_one_cards)
            player_one.add_cards(player_two_cards)
            war_occur = False

        elif player_one_cards[-1].value < player_two_cards[-1].value:
            player_two.add_cards(player_two_cards)
            player_two.add_cards(player_one_cards)
            war_occur = False

        else:
            print('War is happening')

            if len(player_one.all_cards) < number_card_for_war:
                print(f'Player {player_two.name} has won in War!!!')
                game_on = False
                break
            elif len(player_two.all_cards) < number_card_for_war:
                print(f'Player {player_one.name} has won in War!!!')
                game_on = False
                break
            else:
                # Draw number of cards if war occurs
                for index in range(0,3):
                    player_one_cards.append(player_one.remove_one())
                    player_two_cards.append(player_two.remove_one())

