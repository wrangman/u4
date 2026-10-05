import os
import subprocess
import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit  #instans
        self.value = value
            
    def __str__(self):
        return f"{self.suit} {self.value}"
    
    def __repr__(self):                                #mer för utvecklare visa vad klassen innebär
        return f"Card('{self.suit}', {self.value})"


class Deck:
    def __init__(self, cards=None):
        self.cards = cards #instans

    def cards_left(self):
        return len(self.cards)

    def show_all(self):
        for card in self.cards: 
            if card.suit == "♥" or card.suit == "♦": #om det är röda kort ändra färgen på texten med denna ansi-kod
                print(f"\033[31m{card}\033[0m")
            else:
                print(f"{card}")

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left to deal")
        
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]  # Remove dealt cards from the deck
        
        return dealt_cards

    @staticmethod
    def shuffle_deck(cards):
        for c in range(len(cards)):
            # c är ett nummer eller position i kortleken

            r = random.randint(c, len(cards) - 1)  # randint tar med slutvärdet, så -1 för att inte hamna utanför listan

            temp_card = cards[r]

            cards[r] = cards[c]
            cards[c] = temp_card

        return cards
   
    @staticmethod           # en metod som metod likt vanlig metod men en @staticmethod tar inte emot instansen (self) 
    def make_deck():  
        cards = [] 
        suits = ["♠", "♥", "♣", "♦"]
        values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        
        for suit in suits:   # 4 suits
            for value in values: # 13 values per suit
                cards.append(Card(suit, value))    
                
        return cards


class Player():
    def __init__(self, name):
        self.name = name
        self.hand = []

    def take_cards(self, cards):
        self.hand.extend(cards)

    def play_card(self):
        if self.hand:
            return self.hand.pop()
        else:
            return None
        
        #return self.hand.pop() if self.hand else None

    def show_hand(self):
        for card in self.hand:
            print(card)



subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)


# Mappning för att kunna jämföra strängar ("J", "Q", "K", "A") med siffror
card_ranks = {
    2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
    8: 8, 9: 9, 10: 10, "J": 11, "Q": 12, "K": 13, "A": 14
}

# 1. Skapa kortlek och spelare
temp = Deck.make_deck()
cards = Deck.shuffle_deck(temp)

print(cards)
deck = Deck(cards)

player1 = Player("Spelare 1")
player2 = Player("Spelare 2")

while True:
    # 2. Dela ut 1 kort var
    
    player1.take_cards(deck.deal(1))
    c1 = player1.play_card()

    print(f"{player1.name} drog: {c1}")


    player2.take_cards(deck.deal(1))
    c2 = player2.play_card()

    print(f"{player2.name} drog: {c2}")

    # 4. Hämta numeriskt värde och jämför
    v1 = card_ranks[c1.value]
    v2 = card_ranks[c2.value]

    if v1 > v2:
        print(f"{player1.name} vinner med högst kort!")
    elif v2 > v1:
        print(f"{player2.name} vinner med högst kort!")
    else:
        print("Det blev oavgjort!")


    print("Kort kvar: ", deck.cards_left())
    input()






# class Deck:
#     def __init__(self, cards=None): 
#         if cards is None:
#             self.cards = self.make_deck()  # Bygger automatiskt 52 kort om inget skickas in!
#         else:
#             self.cards = cards