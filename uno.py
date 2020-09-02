from dataclasses import dataclass
import random

@dataclass
class Card:
    color: str
    number_action: str
    card_type: str

    def __str__(self):
        return f'{self.color} {self.number_action}'

def Create_Deck():
    colors = ['red', 'green', 'blue', 'yellow']
    digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    actions = ['Skip', 'Reverse', 'Draw Two']
    deck = []
    for n in range(4):
        wild_draw_card = Card('Wild', 'Draw Four', 'action')
        wild_card = Card('Wild', 'Plain', 'action')
        deck.append(wild_draw_card)
        deck.append(wild_card)
    for color in colors:
        zero_card = Card(color, '0', 'digit')
        deck.append(zero_card)

        for digit in digits:
            digit_card = Card(color, digit, 'digit')
            deck.append(digit_card)
            deck.append(digit_card)
    
        for action in actions:
            action_card = Card(color, action, 'action')
            deck.append(action_card)
            deck.append(action_card)

    shuffled_deck = []
    shuffled_deck = shuffled_deck.append(random.shuffle(deck))
    return shuffled_deck

def First_Draw():
    global deck
    hand = []
    for card in range(7):
        hand.append(deck[0])
        del deck[0]
    return hand

def main():
    global deck
    deck = Create_Deck()
    human_hand = First_Draw() 
    playing = True
    print('Welcome to the game of Uno!')
    
    while playing == True:

    


main()