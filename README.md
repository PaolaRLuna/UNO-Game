# Projet-PYTHON
Jeu UNO

## Règles:
Le joueur débute la partie avec 7 cartes. Lorsque c'est son tour, il faut poser une carte portant le même chiffre ou la même couleur que celle qui est sur la table. Quand le joueur place son avant-dernières carte, il doit écrire «UNO».

Après 2 minutes on compte les points et affiche le gagnant.

Le but du jeu: être le premier a ne plus avoir de cartes en main.

### Cartes
- 19 cartes de chaque couleur (bleu, rouge, jaune, verte), numérotées de 0 à 9 (2 pour chaque chiffre sauf pour le 0).

Les cartes spéciales:
* 8 cartes «+2» (2 pour chaque couleur)
* 8 cartes «Inversion/ inversement de sens» (2 pour chaque couleur)
* 8 cartes «Passe ton tour» (2 pour chaque couleur)
* 4 cartes «Joker»
* 4 cartes «+4»

La carte « +2 » :

Lorsqu’un joueur joue cette carte, le joueur suivant doit piocher 2 cartes et passe son tour et cela même si c’est la première carte retournée en début de partie.

La carte « Inversement de sens » :

Lorsqu’un joueur joue cette carte, le sens de la partie est inversée. Si la partie se déroulait dans le sens des aiguilles d’une montre, elle passera donc dans le sens inverse. Même si elle est la première carte retournée en début de partie, elle doit être prise en compte.

La carte « Passe ton tour » :

Lorsqu’un joueur joue cette carte, le joueur suivant doit passer son tour. Même si elle est la première carte retournée en début de partie, elle doit être prise en compte.

La carte « Joker » :

Lorsqu’un joueur joue cette carte, il peut ou non choisir de changer de couleur en l’annonçant aux autre joueurs. Si elle est la première carte retournée en début de partie, le premier joueur choisit donc une couleur.

La carte « +4 » :

Lorsqu’un joueur joue cette carte, le joueur suivant doit piocher 4 cartes et passer son tour. De plus, le joueur qui a posé cette carte peut choisir ou non de changer de couleur. Attention cependant, cette carte ne peut être jouée seulement si le joueur n’a pas d’autre solution. Si un joueur décide de bluffer et qu’il se fait démasquer, il aura alors une pénalité.


««Source (règles):  https://www.regles-de-jeux.com/regle-du-uno/

### Authors
This code has been written in collaboration with @ahguerram and it is the result of our very first incursion into python programming. 
Inspiration comes from Scott Blenkhorne's YouTube video where he explains the logic of the game. We adapted the game following the OOP logic.
This is a console game. Enjoy !
