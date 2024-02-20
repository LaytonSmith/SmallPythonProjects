import random

# Define card colors and values
COLORS = ['Red', 'Yellow', 'Green', 'Blue']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+2', 'Reverse', 'Skip']
WILD_CARDS = ['+4WILD', 'LS']


deck = [(color, value) for color in COLORS for value in VALUES]
deck += [(color, value) for color in COLORS for value in VALUES[1:]]  # Skip '0' for non-neutral colors
deck += [(color, 'Reverse') for color in COLORS]
deck += [(color, 'Skip') for color in COLORS]
deck += [(color, '+2') for color in COLORS]
deck += [(WILD, 'Wild') for WILD in WILD_CARDS] * 4  # 4 copies of each Wild card

# Shuffle the deck
random.shuffle(deck)

def deal_hand(num_cards):
    """Deal a hand of cards to each player."""
    return [deck.pop() for _ in range(num_cards)]

def can_play(card, top_card, current_direction):
    """Check if a card can be played based on Uno rules."""
    color, value = card
    top_color, top_value = top_card

    if current_direction == 1:  # Reverse direction
        return color == top_color or value == top_value or value == 'Reverse' or value in WILD_CARDS
    else:
        return color == top_color or value == top_value or value in WILD_CARDS

def main():
    print("""UnoMyWay Github: https://github.com/LaytonSmith\nRules: 
          Typical Uno rules, Cards stack if you have two of the same number.
          LS(life saver) card works as follows; when you draw it, you can set it down right away and pick any card in the deck to set down as well if you want.""")

    num_players = int(input("Enter the number of players: "))
    players = {f'P{i + 1}': deal_hand(5) for i in range(num_players)}

    top_card = deck.pop()  # Draw the first card from the deck
    print("Top Card:", top_card)

    current_player = 0
    current_direction = 1  # 1 for forward, -1 for reverse
    while True:
        player_name = f'P{current_player + 1}'
        print(f"\n{player_name}'s Turn")
        print(f"{player_name}'s Hand: {players[player_name]}")
        print("Top Card:", top_card)

        playable_cards = [card for card in players[player_name] if can_play(card, top_card, current_direction)]

        if not playable_cards:
            print(f"{player_name} has no playable cards. Drawing a card.")
            drawn_card = deck.pop()
            players[player_name].append(drawn_card)
            print(f"{player_name} drew {drawn_card}")

        else:
            print(f"Playable Cards: {playable_cards}")
            chosen_card = input(f"Choose a card to play: ").upper()
            if chosen_card not in [str(card) for card in playable_cards]:
                print("Invalid choice. Try again.")
                continue
            if chosen_card == 'QUIT':
                print('Thanks 4 playing!')
                sys.exit()
            players[player_name].remove(playable_cards[0])
            top_card = playable_cards[0]
            print(f"{player_name} played {top_card}")

            if not players[player_name]:
                print(f"{player_name} has no cards left. {player_name} wins!")
                break

            if top_card[1] == '+4WILD':
                chosen_color = input("Choose a color (Red, Yellow, Green, Blue): ").capitalize()
                top_card = (chosen_color, '+4WILD')

            elif top_card[1] == 'Reverse':
                current_direction *= -1  # Reverse the direction

            current_player = (current_player + current_direction) % num_players
            

def display_card(card):
    color, value = card

    card_str = f"""
    +-----+
    | {value.center(4)} |
    |  {color[:1]}  |
    +-----+
    """

    print(card_str)


def display_hand(hand):
    for card in hand:
        display_card(card)
        
if __name__ == "__main__":
    main()
