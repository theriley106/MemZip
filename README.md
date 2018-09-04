# KPCB_Fellows_Application
Simple Multiplayer Memory game for my KPCB Fellowship application


## Overview

MemZip is a multiplayer card memorization game, where users can compete against each other to see who can memorize the most playing cards.

High Scores are recorded externally, so you can play against your friends!

The rules are simple - a group of randomly selected playing cards
will display in the terminal.  You have to respond with the correct order
of cards to progress through the game.

The number of cards to memorize will increment as each round completes.
To make the challenge harder, the time to look at the cards will decrease each round.


## Technical Overview

### Frontend

The project was limited to a terminal-based game, so images of playing cards were unfortunately out of the question.

I considered many alternatives for the card displays, but ultimately decided that creating my own text art would be the best way to approach the problem.  Using UTF-8 Characters, I was able to create the look of a regular playing card with a specified height and width - this created a string that was visually similar to a standard playing card.

You can see in card.py, there is a function known as card.create_cards(), which takes a list of dictionaries defining the "Type" and "Suit" of the card and returns a string.





### Backend

The
