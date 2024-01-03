import blackjack_class
import blackjack_func

keep_playing = True

#Gen player's chip
player_chip = blackjack_class.Chip(5000)

while keep_playing:
    player_bursts_flag = False
    dealer_bursts_flag = False
    # Gen a deck
    game_deck = blackjack_class.Deck()
    game_deck.shuffle()

    # Gen playeer and dealer
    player_hand = blackjack_class.Hand()
    dealer_hand = blackjack_class.Hand()


    # Place first bet
    bet_chips = blackjack_func.take_bet(player_chip)
    if bet_chips == 0:
        break
    # First deal
    player_hand.add_card(game_deck.deal_one())
    dealer_hand.add_card(game_deck.deal_one())
    player_hand.add_card(game_deck.deal_one())
    dealer_hand.add_card(game_deck.deal_one())

    blackjack_func.show_some(player_hand, dealer_hand)

    while True:
        playing_check = blackjack_func.hit_or_stand(game_deck, player_hand)
        if playing_check == 'hit':
            blackjack_func.show_some(player_hand, dealer_hand)
            if player_hand.hand_value > 21:
                blackjack_func.player_bursts(player_hand, dealer_hand, player_chip)
                player_bursts_flag = True
                break
        else:
            break

    blackjack_func.show_all(player_hand, dealer_hand)
    if player_bursts_flag == True:
        pass
    else:
        while (dealer_hand.hand_value < 17):
            blackjack_func.hit(game_deck, dealer_hand)
            blackjack_func.show_all(player_hand, dealer_hand)
        if dealer_hand.hand_value > 21:
            blackjack_func.dealer_bursts(player_hand, dealer_hand, player_chip)
        elif dealer_hand.hand_value > player_hand.hand_value:
            blackjack_func.dealer_wins(player_hand, dealer_hand, player_chip)
        elif dealer_hand.hand_value < player_hand.hand_value:
            blackjack_func.player_wins(player_hand, dealer_hand, player_chip)
        else:
            blackjack_func.tie(player_hand, dealer_hand)

    print(f"$$$ Your chips are: {player_chip.pocket}")
    if (player_chip.pocket == 0):
        print("You were kicked out from the Casino ..........")
        break
    # keep_playing = blackjack_func.play_again()

