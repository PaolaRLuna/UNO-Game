import random

class Carte:

    def __init__(self, couleur, number):
        self.couleur = couleur
        self.num = number

    def __str__(self):
        return f"{self.couleur} {self.num}"

class Paquet:

    def __init__(self):
        COULEURS = ["Blue", "Green", "Red", "Yellow"]
        NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+2", "Inversion", "Passer"]
        WILDS = ["Joker", "Joker +4"]
        self.card_deck = []
        for col in COULEURS:
            for val in NUMBERS:
                carte = f"{Carte(col, val)}"
                self.card_deck.append(carte)
                if val != 0:
                    carte = f"{Carte(col, val)}"
                    self.card_deck.append(carte) 
        
        for i in range(4):
            self.card_deck.append(WILDS[0])
            self.card_deck.append(WILDS[1])
        
    def brassage_inter(self):
        half = len(self.card_deck) // 2
        paquet1 = self.card_deck[:half]
        paquet2 = self.card_deck[half:]

        deck_brasse = []
        for i in range(len(paquet1)):
            deck_brasse.append(paquet1[i])
            deck_brasse.append(paquet2[i])
        self.card_deck = deck_brasse

    def pop(self):
        return self.card_deck.pop()

    def brassage_paquets(self):
        len_cartes = len(self.card_deck)
        deck_brasse = []
        for i in range(0, len_cartes, 8):
            deck_de_huit = self.card_deck[i : i + 8]
            deck_brasse.append(deck_de_huit)

        order = [7, 1, 3, 13, 2, 4, 11, 6, 8, 5, 12, 10, 9, 14]
        deck_brasse_update = []
        for idx in order:
            paquet = deck_brasse[idx-1]
            deck_brasse_update.extend(paquet)

        self.card_deck = deck_brasse_update

    def brassage_multiple(self):
        brassages = [self.brassage_inter, self.brassage_paquets]
        for i in range(random.randint(0, 8)):
            brassages[random.randint(0,1)]()
        
        random.shuffle(self.card_deck)
        CONDITION_DEPART = ["Joker","Inversion", "Passer", "+2", "+4"]  
        n = 1
        for i in CONDITION_DEPART:
            while i in self.card_deck[-1]:
                self.card_deck = self.card_deck[-1:] + self.card_deck[:-1] #https://www.geeksforgeeks.org/python-shift-last-element-to-first-position-in-list/
                n += 1
        return self.card_deck
             
    def draw_cards(self, num_cartes): 
        cartes_retire = []
        for c in range(num_cartes):
            cartes_retire.append(self.card_deck.pop(0))
        return cartes_retire

    def discard_pile(self):
        discards = []
        discards.append(self.card_deck.pop(-1))
        return discards


class Jeu:   

    def __init__(self):
        self.new_deck = Paquet()      
   
    def welcome_players(self):
        self.new_deck.brassage_multiple()

        players_hands = []
        print("************UNO GAME*************")

        sortie = False
        self.nb_joueurs = int(input("Combien de joueurs ? : "))
        while not sortie:
            if 2 <= self.nb_joueurs <= 4:
                sortie = True
            else:
                self.nb_joueurs = int(input("Vous pouvez juste jouer entre 2 et 4 joueurs. Combien de joueurs ?: "))

        for player in range(self.nb_joueurs):
            players_hands.append(self.new_deck.draw_cards(7))

        return players_hands

    def gameloop(self):
        self.playerturn = 0
        self.jeu_direction = 1
        self.players_hands = self.welcome_players()

        playing = True
        self.discards_cards = self.new_deck.discard_pile()

        while playing:
            self.player_hand = self.players_hands[self.playerturn]
            joueur = Turn(self.playerturn, self.player_hand, self.jeu_direction, self.new_deck, self.discards_cards)
            print(joueur)
            print(f"Carte au dessus du talon visible : {self.discards_cards[-1]}")

            colour, value = joueur.splitcard()
            if joueur.can_play(colour, value):
                self.cartes_joue(colour, value, joueur)
            
                if len(joueur.player_hand) == 0:
                    playing = False
                    print(f"Le gagnant est le joueur # {self.playerturn + 1}. Félicitations !")                   
                else:
                    self.recheck_card_chosen(joueur)
            else:
                print("Vous ne pouvez pas jouer, vous devez retirer une carte.\n")
                self.player_hand = self.player_hand + joueur.pioche_cartes(1) 
                self.players_hands[self.playerturn] = self.player_hand
            self.game_direction()
        
    def game_direction(self):
        self.playerturn += self.jeu_direction
        if self.playerturn == self.nb_joueurs:
            self.playerturn = 0
        elif self.playerturn < 0:
            self.playerturn = self.nb_joueurs - 1

    def cartes_joue(self, colour, value, joueur):
        carte_choisie = int(input("Quelle carte voulez vous jouer ?: "))
        while not joueur.can_play(colour, value, self.player_hand[carte_choisie-1]):
            carte_choisie = int(input("Carte invalide. Quelle carte voulez vous jouer ?: "))
        print(f"Vous avez joué ***{joueur.player_hand[carte_choisie-1]}***\n")
        self.discards_cards.append(joueur.remove_fromhand(carte_choisie))

    def recheck_card_chosen(self, joueur):
        SPECIAL = ["+2", "Inversion", "Passer", "Joker"]
        colour, value = joueur.splitcard()
        if colour == "Joker":
            colour, value = joueur.check_joker_card()
            self.discards_cards[-1] = (colour + ' ' + value)
        elif colour == "Joker" and value == "+4":
            colour, value = joueur.check_joker_card()
            self.discards_cards[-1] = (colour + ' ' + value)
            self.gerer_special_cards(value)
        elif value in SPECIAL:
            self.gerer_special_cards(value)

    def gerer_special_cards(self, value):
        if value == "Inversion":
            self.jeu_direction = self.jeu_direction * -1
        elif value == "Passer":
            self.game_direction()
        elif value == "+2":
            self.next_player_draws(2)
            self.game_direction()
        elif value == "+4":
            self.next_player_draws(4)

    def next_player_draws(self, cards):
        playerdraw = self.playerturn + self.jeu_direction
        if playerdraw == self.nb_joueurs:
            playerdraw = 0
        elif playerdraw < 0:
            playerdraw = self.nb_joueurs - 1
        carte = []
        for i in range(cards):
            carte.append(self.new_deck.pop())
        self.players_hands[playerdraw] += carte


class Turn:

    def __init__(self, player, p_hand:list, direction, whole_deck:list, discards_cards:str) -> None:
        self.player_hand = p_hand
        self.player = player
        self.direction = direction
        self.all_deck = whole_deck
        self.discards_cards = discards_cards

    def splitcard(self): 
        splitcard = self.discards_cards[-1].split(" ", 1)
        currentcolour =  splitcard[0]
        if currentcolour != "Joker":
            cardval = splitcard[1]
        else:
            cardval = "Any"
        return currentcolour, cardval

    def check_joker_card(self): 
        currentcolour = self.discards_cards[-1]
        if currentcolour == "Joker":
            cardval = currentcolour
            currentcolour = self.choose_special_card()
        elif currentcolour == "Joker +4":
            splitcard = currentcolour.split(" ", 1)
            cardval = splitcard[0]
            currentcolour = self.choose_special_card()
        return currentcolour, cardval

    def can_play(self, colour, value, trytoplay_lst = []):         

        if len(trytoplay_lst) == 0:
            for card in self.player_hand:
                if "Joker" in card:
                    return True
                elif colour in card or value in card:
                    return True
            return False
        else:
            trytoplay_lst = trytoplay_lst.split(" ")
            for card in trytoplay_lst:
                if "Joker" in card:
                    return True
                elif colour in card or value in card:
                    return True
            return False

    def remove_fromhand(self, carte_choisie):
        return self.player_hand.pop(carte_choisie - 1)

    def choose_special_card(self):
        colors = ["Blue", "Green", "Red", "Yellow"]
        for pos in range(len(colors)):
            print(f"{pos + 1}🀡 {colors[pos]}")
        sortie = False
        while not sortie:
            newcolor = int(input("Quel couleur voulez vous choisir ? : "))
            if 1 <= newcolor <= 4 :
                sortie = True
                currentcolor = colors[newcolor-1]
            else:
                newcolor = int(input("Choix invalide. vous devez rentrer un numero entre 1 et 4: "))
        print(f"\nVous avez choisi {currentcolor}\n")
        return currentcolor

    def pioche_cartes(self, num_cartes): 
        cartes_retire = []
        for c in range(num_cartes):
            card_deck = self.all_deck
            carte_pioche = card_deck.pop()
            cartes_retire.append(carte_pioche)
        return cartes_retire

    def __str__(self) -> str:
        nb_carte = 1
        cartes = []
        for card in self.player_hand:
            carte = str(nb_carte) + "🀡  " + card
            cartes.append(carte)
            nb_carte += 1
        return f"Player {self.player + 1} 's Turn\n" + f"\n Ves cartes sont: \n" + "\n".join(i for i in cartes) + "\n"


game = Jeu()
game.gameloop()


