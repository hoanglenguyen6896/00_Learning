# import blackjack_class

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input(f"You have {chips.pocket}. Place you bet (0 to quit):\n\t>> "))
        except:
            print("Invalid input!!!")
        else:
            if chips.bet > chips.pocket:
                print("Sorry, you only have {chips.pocket} ...")
            else:
                return chips.bet
                break

def hit(deck, hand):
    hand.add_card(deck.deal_one())
    hand.aces_adjuct()

def hit_or_stand(deck, hand):

    while True:
        x = input("Hit or Stand (Enter 'h' or 's')?\n\t>> ")

        if x[0].lower() == 'h':
            hit(deck, hand)
            return 'hit'
        elif x[0].lower() == 's':
            print("Player Stands. Dealer's Turn")
            return 'stand'

        else:
            print("Sorry, please try again ...")
            continue

# Show one dealer's card, all player's card
def show_some(player, dealer):

    # Show dealer's card: 1 up, 1 down
    print(f"{'Dealer cards':=^80}")
    print(f"{'Hidden!': >80}")
    print("{temp: >80}".format(temp = dealer.current_hand[1].__str__()))
    # Show all card
    print(f"{'Player cards':=^80}")
    for card in player.current_hand:
        print(card)
    print(f"\t>>>>> Player's value: {player.hand_value}")
    print(f"{'':=^80}")

def show_all(player, dealer):
    # Show all dealer's card
    print(f"{'Dealer cards':=^80}")
    for card in dealer.current_hand:
        print("{temp: >80}".format(temp = card.__str__()))
    print(f"\t>>>>> Dealer's value: {dealer.hand_value}")
    # Show all player's card
    print(f"{'Player cards':=^80}")
    for card in player.current_hand:
        print(card)
    """
    Method 2 to print a list:

    print(f"Say something: \n", *your_list, sep='separate by this str')

    """
    print(f"\t>>>>> Player's value: {player.hand_value}")
    print(f"{'':=^80}")

def player_bursts(player, dealer, chips):
    print("****************************")
    print("******> Player BUSTS< ******")
    print("****************************")
    chips.lose()

def player_wins(player, dealer, chips):
    print("****************************")
    print("******> Player WINS <*******")
    print("****************************")
    chips.win()

def dealer_bursts(player, dealer, chips):
    print("****************************")
    print("******> Dealer BUSTS <******")
    print("****************************")
    chips.win()

def dealer_wins(player, dealer, chips):
    print("****************************")
    print("******> Dealer WINS <*******")
    print("****************************")
    chips.lose()

def tie(player, dealer):
    print("****************************")
    print("******> TIE !!!!!!!! <******")
    print("****************************")

def play_again():
    flag = input("Play again (Y or N): ")
    if flag[0].upper() == 'Y':
        return True
    elif flag[0].upper() == 'N':
        return False
