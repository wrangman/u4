def play_game():
    # Mappning för att kunna jämföra strängar ("J", "Q", "K", "A") med siffror
    card_ranks = {
        2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
        8: 8, 9: 9, 10: 10, "J": 11, "Q": 12, "K": 13, "A": 14
    }

    # 1. Skapa kortlek och spelare
    cards = Deck.make_deck()
    deck = Deck(cards)
    
    player1 = Player("Spelare 1")
    player2 = Player("Spelare 2")

    # 2. Dela ut 1 kort var
    player1.take_cards(deck.deal(1))
    player2.take_cards(deck.deal(1))

    # 3. Spela ut korten
    c1 = player1.play_card()
    c2 = player2.play_card()

    print(f"{player1.name} drog: {c1}")
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