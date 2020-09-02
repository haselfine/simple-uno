from dataclasses import dataclass
import random
import sys
import time

#since user turn is determined by % 2, the user always starts first
turn_num = 2 

@dataclass
class Card:
    color: str
    number_action: str
    card_type: str

    def __str__(self):
        return f'{self.color} {self.number_action}' #users don't need to see card_type

def main():
    global deck
    global pile
    global human_hand
    global comp_hand

    deck = create_deck()
    human_hand = first_draw()
    comp_hand = first_draw()
    pile = create_pile()
    print('Welcome to the game of Uno!')
    begin()


def create_deck():
    #108 cards in deck

    colors = ['Red', 'Green', 'Blue', 'Yellow']
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    actions = ['Skip', 'Reverse', 'Draw-Two']
    deck = []

    for n in range(4): #four of each Wild
        wild_draw_card = Card('Wild', 'Draw-Four', 'action')
        wild_card = Card('Wild', '(plain)', 'action')
        deck.append(wild_draw_card)
        deck.append(wild_card)

    for color in colors: #one 0 card per color
        zero_card = Card(color, '0', 'digit')
        deck.append(zero_card)

        for digit in digits: #two number cards each per color
            digit_card = Card(color, digit, 'digit')
            deck.append(digit_card)
            deck.append(digit_card)
    
        for action in actions: #two action cards each per color
            action_card = Card(color, action, 'action')
            deck.append(action_card)
            deck.append(action_card)

    random.shuffle(deck) #randomize order
    return deck

def first_draw(): #determine first cards in hand
    global deck
    hand = []
    for n in range(1): #only one card to start, just to simplify testing
        hand.append(deck[0])
        del deck[0] #remove card from top of deck
    return hand

def create_pile(): #pile is where players put their matches
    global deck 
    first = deck[0]
    del deck[0]
    while first.card_type != 'digit': #loops to make sure first card is both a digit and a color
        first = deck[0]
        del deck[0]
    return first

def check_actions(hand): #determines what players are able to do
    actions = ['Draw']
    for card in hand: #search for matches in hand
        if card.color == pile.color or card.number_action == pile.number_action:
            actions.append(f'Play {card}')
        elif card.color == 'Wild': #wild cards can always be played
            actions.append(f'Play {card}')
    
    if turn_num % 2 == 0: #add quit option for user
        actions.append('Quit')
    return actions

def begin(): #I added this just so there isn't a mountain of text the moment the user opens the program
    begin_q = input('Would you like to play? "y" or "n"?  ')
    if begin_q == 'y':
        play()
    elif begin_q == 'n':
        sys.exit
    else:
        print('You must enter "y" or "n".')
        begin()

def play(): #most of the program stays in this function
    global turn_num

    if turn_num % 2 == 0: #user plays on even turns, always first
        print('\n****YOUR TURN****')    
        human_turn()
        turn_num += 1
        time.sleep(1) #slows the terminal text down so user can more easily follow what's happening
    else:
        print('\n****COMPUTER\'S TURN****')
        comp_turn()
        turn_num +=1
        time.sleep(1)
    if len(human_hand) == 0: #check if user has cards, ends loop
        print('Congratulations! You won!!')
    elif len(comp_hand) == 0: #check if computer has cards, ends loop
        print('Computer wins. Game over.')
    elif len(deck) == 0: #if deck has no more cards, whoever has less cards in hand wins
        no_more_cards()
    else:
        play() #loop

def human_turn():
    global human_hand
    while True: #loop makes sure user does appropriate action
        print(f'\n# OF CARDS IN COMPUTER\'S HAND: {len(comp_hand)}')
        print('\nYOUR HAND: ')
        for card in human_hand:
            print(card)
        time.sleep(1) #once again slows terminal so user can follow more easily

        if(len(human_hand) == 1):
            print('\nUno!')
            time.sleep(1)

        print(f'\nCARD ON PILE: {pile}')
        time.sleep(1)
        
        actions = check_actions(human_hand)
        print('\nAVAILABLE ACTIONS: ')
        for action in range(len(actions)):
            print(f'{action}: {actions[action]}')
        
        try:
            choice = int(input('\nWhat do you choose? (choose from numbers above): ')) #user must make choice between numbered actions
        except ValueError: #prevents crash due to improper input
            print('Sorry, your answer must be in digit form.')
            continue

        if choice < 0: #validate
            print('Sorry, your answer cannot be a negative number')
            continue
        elif choice >= len(actions): #validate
            print('Sorry, your answer exceeds the number of choices.')
            continue
        elif choice == 0: #drawing is always first option
            human_hand = draw(human_hand)
            break
        elif choice == len(actions)-1: #quitting is always last option
            sys.exit()
        else: #user chooses a card from hand
            human_hand = add_to_pile(human_hand, actions[choice])
            print(f'CARD ON PILE IS NOW {pile}')
            break

def draw(hand):
    global deck
    if len(deck)>0: #make sure deck has cards
        hand.append(deck[0])
        if(turn_num % 2 == 0): #if user's turn, inform of new cards one by one
            print(f'YOU DREW {deck[0]}.')
            time.sleep(1)
        del deck[0] #remove card from top of deck
        return hand
    else:
        no_more_cards()

def add_to_pile(hand, action):
    action_to_card = action[5:] #since the action always starts with "Play ", I'm removing that so we just get color and number
    new_pile = action_to_card.split() #convert to list of color [0] and number [1]
    for card in hand:
        if card.color == new_pile[0] and card.number_action == new_pile[1]: #match player choice to the card in their hand
            global pile
            pile = card #update pile to chosen card
            if card.card_type == 'action': #if card requires action, perform action
                perform_action(card)
            del hand[hand.index(card)] #remove from hand
            return hand
    
def perform_action(card):
    global turn_num
    global comp_hand
    global human_hand

    if card.number_action == 'Skip' or card.number_action == 'Reverse': #since there's only 2 players, these cards just give the current player an extra turn
        turn_num += 1
    elif card.number_action == 'Draw-Two':
        for n in range(2):
            if turn_num % 2 == 0:
                draw(comp_hand)
            else:
                draw(human_hand)
    elif card.number_action == 'Draw-Four':
        for n in range(4):
            if turn_num % 2 == 0:
                draw(comp_hand)
            else:
                draw(human_hand)

    if card.color == 'Wild': #color must be chosen by player
        if turn_num % 2 == 0:
            choose_color_human()
        else:
            choose_color_comp()

def choose_color_human(): 
    global pile
    while True: #user must choose a valid color
        print('Choose a color: Red, Blue, Green, or Yellow.')
        color = input('What is your choice? ')
        if color.lower() == 'red':
            pile.color = 'Red'
            break
        elif color.lower() == 'blue':
            pile.color = 'Blue'
            break
        elif color.lower() == 'green':
            pile.color = 'Green'
            break
        elif color.lower() == 'yellow':
            pile.color = "Yellow"
            break
        else:
            print('Your choice must be one of the colors below.')
            continue

def choose_color_comp(): #computer doesn't choose intelligently. Just random
    global pile
    number = random.randint(0, 3)
    if number == 0:
        pile.color = 'Red'
    elif number == 1:
        pile.color = 'Blue'
    elif number == 2:
        pile.color = 'Green'
    else:
        pile.color = 'Yellow'

def no_more_cards(): #just in case deck loses all cards. I decided against reshuffling, because then the program would have to remember every card in the pile
    print('No more cards in deck.\nWinner is whoever has less cards in hand...')
    if len(human_hand) > len(comp_hand):
        print('You have less cards! You win!!')
        sys.exit()
    else:
        print('Computer has less cards. Computer wins.')
        sys.exit()

def comp_turn():
    global comp_hand
    if(len(comp_hand) == 1): #check for uno
            print('COMPUTER SAYS: "Uno!"')
            time.sleep(1)
    actions = check_actions(comp_hand)
    actions.reverse() #makes sure drawing is last option for computer
    print(f'Computer chooses to {actions[0]}.') #inform user of computer choice
    time.sleep(1)
    if actions[0] == 'Draw':
        comp_hand = draw(comp_hand)
    else:
        add_to_pile(comp_hand, actions[0])

main()