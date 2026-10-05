import os
import random
import subprocess


class Card:
    # Rangordning för att kunna jämföra bokstäver ("J", "Q", "K", "A") med siffror. Ess är högst.
    RANKS = {
        2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
        8: 8, 9: 9, 10: 10, "J": 11, "Q": 12, "K": 13, "A": 14
    }

    def __init__(self, suit, value):
        self.suit = suit  # instansattribut
        self.value = value

    def rank(self):
        return Card.RANKS[self.value]

    def __lt__(self, other):  # gör att man kan skriva kort1 < kort2
        return self.rank() < other.rank()

    def __gt__(self, other):  # gör att man kan skriva kort1 > kort2
        return self.rank() > other.rank()

    def __str__(self):  # för användaren: det som syns vid print()
        text = f"{self.suit} {self.value}"
        if self.suit == "♥" or self.suit == "♦":  # röda kort får röd text med en ANSI-kod
            return f"\033[31m{text}\033[0m"
        return text

    def __repr__(self):  # för utvecklare: visar hur objektet skapas
        return f"Card({self.suit!r}, {self.value!r})"


class Deck:
    def __init__(self, cards=None):
        if cards is None:
            cards = Deck.make_deck()  # bygger automatiskt 52 kort om inget skickas in
        self.cards = cards  # instansattribut

    def cards_left(self):
        return len(self.cards)

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Inte tillräckligt många kort kvar")

        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]  # ta bort de utdelade korten från leken

        return dealt_cards

    def shuffle(self):
        for c in range(len(self.cards)):
            # c är en position i kortleken

            r = random.randint(c, len(self.cards) - 1)  # randint tar med slutvärdet, så -1 för att inte hamna utanför listan

            temp_card = self.cards[r]

            self.cards[r] = self.cards[c]
            self.cards[c] = temp_card

    @staticmethod  # en metod som hör till klassen men inte tar emot instansen (self)
    def make_deck():
        cards = []
        suits = ["♠", "♥", "♣", "♦"]
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]

        for suit in suits:  # 4 färger
            for value in values:  # 13 valörer per färg
                cards.append(Card(suit, value))

        return cards


def ask_bet():
    legal_moves = ["H", "L", "A"]

    while True:
        bet = input("(H)ögre, (L)ägre eller (A)vsluta? ").strip().upper()
        if bet in legal_moves:
            return bet
        print("Ogiltigt val, försök igen.")


def play_round():
    # 1. Skapa och blanda en ny kortlek varje omgång (den gamla tar Python bort automatiskt)
    deck = Deck()
    deck.shuffle()

    # 2. Första kortet blir referens
    current = deck.deal(1)[0]
    score = 0

    while deck.cards_left() > 0: #game loop
        print(f"Kortet är: {current} (kort kvar: {deck.cards_left()})")

        # 3. Spelaren gissar
        bet = ask_bet()
        if bet == "A":
            break

        # 4. Vänd nästa kort och jämför
        next_card = deck.deal(1)[0]
        print(f"Nästa kort: {next_card}")

        if (bet == "H" and next_card > current) or (bet == "L" and next_card < current):
            score += 1
            print("Rätt!\n")
        else:
            print("Fel! Omgången är slut.\n")
            break

        if deck.cards_left() == 0:
            print("Slut på kort – du klarade hela leken!\n")

        current = next_card  # det nya kortet blir referens för nästa gissning

    return score


best = 0

while True: #main loop
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

    print("HÖGRE ELLER LÄGRE")
    print("Gissa om nästa kort är högre eller lägre. Ess är högst och lika kort räknas som fel.\n")

    score = play_round()
    best = max(best, score)
    print(f"Du fick {score} rätt i rad. Bästa hittills: {best}")

    again = input("Spela igen? (J/N) ").strip().upper()
    if again != "J":
        break


