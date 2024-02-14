import random, sys

# Set up the constants:
HEARTS  = chr(9829)
DIAMONDS    = chr(9830)
SPADES  = chr(9824)
CLUBS   = chr(9827)
    # How to use the chr() function in Python https://www.programiz.com/python-programming/methods/built-in/chr

BACKSIDE = 'backside'


def main(): 
        print('''Blackjack! Github: https://github.com/LaytonSmith
              
              Rules:
                Try to get as close ot 21 wihtout going over.
                Kings, Queens, and Jacks are worth 10 points.
                Aces aare worth 1 or 11 points.
                Cards 2 through 10 are worth their face value.
                (H)it to take another card.
                (S)tand to stop taking cards.
                On your first play, you can (D)ouble down, but you have to hit exactly one more time before standing.
                In case of a tie, the bets will be returned.
                The dealer stops hitting at 17.''')
        
        money = float(input("Enter the amount you want to start with: "))
        while True: #Main game loop.
            # checking if player ran out of money --
            if money <= 0:
                print("You're such a brokie")
                print("U lost, too bad, so sad")
                print('Try again later tho.')
                sys.exit()
                
                
            # where player enters the bet
            
            print('Money:', money)
            bet = getBet(money)
            
            # Two cards given to the dealer and player each from the deck:
            deck = getDeck()
            dealerHand = [deck.pop(), deck.pop()]
            playerHand = [deck.pop(), deck.pop()] 
            
            #handle player actions:
            print('Bet:', bet)
            while True: # Loops until player stands or busts.
                displayHands(playerHand, dealerHand, False)
                print()
                
                # Check if the player has a bust:
                move = getMove(playerHand, money - bet)
                
                # Handle the player actions:
                if move == 'D':
                    # Player is doublig down, they can increase their bet:
                    additionalBet = getBet(min(bet, (money - bet)))
                    bet += additionalBet
                    print('Bet increased to {}.'.format(bet))
                    print('Bet:', bet)
                    
                if move in ('H', 'D'):
                    # hit/doubling down takes another card.
                    newCard = deck.pop()
                    rank, suit = newCard
                    print('You drew a {} of {}.'.format(rank, suit))
                    playerHand.append(newCard)
                    
                    if getHandValue(playerHand) > 21:
                        #the player has busted:
                        continue
                    
                if move in ('S', 'D'):
                    # Stand/ doubling down stops the players turn.
                    break
                
            # Handle the dealers actions:
            if getHandValue(playerHand) <= 21:
                while getHandValue(dealerHand) < 17:
                    # The dealer hits:
                    print('Dealer hits...')
                    dealerHand.append(deck.pop())
                    displayHands(playerHand, dealerHand, False)
                    
                    if getHandValue(dealerHand) > 21:
                        break # The dealer has buste.
                    input('Press Enter to continue...')
                    
                    print('\n\n')
                    
            # this shows the final hands:
            displayHands(playerHand, dealerHand, True)
            
            playerValue = getHandValue(playerHand)
            dealerValue = getHandValue(dealerHand)
            # handle wheather the player won, lost, or tied:
            if dealerValue > 21:
                print('Dealer busts! You win ${}!'.format(bet))
                money += bet
            elif (playerValue > 21) or (playerValue < dealerValue):
                print('You lost money.. Kinda Cringe bro')
                money -= bet 
            elif playerValue > dealerValue:
                print('You won ${}!'.format(bet))
                money += bet
            elif playerValue == dealerValue:
                print('It\'s a tie, money is returned.')
                
            input('Press Enter to continue...')
            print('\n\n')
            
            
            
def getBet(maxBet):
    """Ask the player how much they want to bet for this round """
    while True:     #keep asking until they enter a valid amount.
        print('How much u wanna bet? (1-{}, (V)iew Bet History, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks 4 playing!')
            sys.exit()
        if bet == 'V':
            print(bet_history)
            if bet_history == '':
                return bet
        if not bet.isdecimal():
            continue    # If the player didn't enter a number, ask again.
            
        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet      #player entered a valid bet.
            
def getDeck():
    """Return a list of (rank, suit) tuples for all 52 cards"""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))      #Add the face and ace cards.
    random.shuffle(deck)
    return deck


def displayHands(playerHand, dealerHand, showDealerHand):
    """Show the plauyers and dealers cards. Hide the dealers first card if showDealerHand is False."""
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    
    else:
        print('DEALER: ?????')
        # Hide the dealers first card:
        displayCards([BACKSIDE] + dealerHand[1:])
        
    # Show the plyers cards:
    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)


def getHandValue(cards):
    """Returns the value of the cards. Face cards are worth 10, aces are worth 11 or 1 (this function picks the most suitable ace value)."""
    value = 0
    numberOfAces = 0
    
    # Add the value for the non-ace cards:
    for card in cards:
        rank = card[0]  # card is a tuple like (rank, suit)
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'): #Face cards are worth 10 points.
            value +=10
        else:
            value += int(rank) # numbered cards are worth their number.
            
    #add the value for the aces:
    value += numberOfAces   # Add 1 per ace
    for i in range(numberOfAces):
        #if anotherr 10 can be added with busting, do so:
        if value + 10 <= 21:
            value += 10
            
    return value



def displayCards(cards):
    """Display all the cards in the cards list"""
    rows = ['', '', '', '', '']  # the texrt to display on each row.
    
    for i , card in enumerate(cards):
        rows[0] += ' ___  ' # Print the top line of the card.
        if card == BACKSIDE:
            # Print a cards back:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print the cards front:
            rank, suit = card 
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))
        
    # print the rows on the screen
    for row in rows:
        print(row)
        
        
def getMove(playerHand, money):
    """Asks the player for their move, and returns 'H' for hit, 'S' for stand, and 'D' for doble down."""
    while True:     #keep looping until the player enters a correct move
        moves = ['(H)it', '(S)tand']
        
        # the player can double down on their first move, which we can tell because they will have exacttly two cards:
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')
            
            # get the players move:
        movePrompt = ',  '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            return move # Player has entered a value move
        if move == 'D' and '(D)ouble down' in moves:
            return move #Player has entered a value move.
        
bet_history = []


def main():
    global bet_history  # Declare bet_history as a global variable

    money = float(input("Enter the amount you want to start with: "))
    while True:  # Main game loop.
        # checking if player ran out of money --
        if money <= 0:
            print("You're such a brokie")
            print("U lost, too bad, so sad")
            print('Try again later tho.')
            sys.exit()

        # where player enters the bet
        print('Money:', money)
        bet = getBet(money)
        bet_history.append(bet)  # Record the bet in the history

        # Two cards given to the dealer and player each from the deck:
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # handle player actions:
        print('Bet:', bet)
        while True:  # Loops until the player stands or busts.
            displayHands(playerHand, dealerHand, False)
            print()

            # Check if the player has a bust:
            move = getMove(playerHand, money - bet)

            # Handle the player actions:
            if move == 'D':
                # Player is doubling down, they can increase their bet:
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}.'.format(bet))
                print('Bet:', bet)

            if move in ('H', 'D'):
                # hit/doubling down takes another card.
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # the player has busted:
                    continue

            if move in ('S', 'D'):
                # Stand/ doubling down stops the player's turn.
                break

        # Handle the dealer's actions:
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # The dealer hits:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break  # The dealer has busted.
                input('Press Enter to continue...')

                print('\n\n')

        # this shows the final hands:
        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        # handle whether the player won, lost, or tied:
        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost money.. Kinda Cringe bro')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('It\'s a tie, money is returned.')

        # Display bet history after each round
        print('\nBet History:')
        for i, bet_amount in enumerate(bet_history, start=1):
            print(f"Round {i}: ${bet_amount}")

        input('Press Enter to continue...')
        print('\n\n')



if __name__ == '__main__':
    main()            