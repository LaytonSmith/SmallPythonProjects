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
        
        money = 5000
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
        print('How much u wanna bet? (1-{}, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks 4 playing!')
            sys.exit()
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
        