# KPCB_Fellows_Application
Simple Multiplayer Memory game for my KPCB Fellowship application


## Overview

MemZip is a multiplayer card memorization game where users can compete against each other to see who can memorize the most playing cards.

High Scores are recorded externally, so you can play against your friends!

The rules are simple - a group of randomly selected playing cards
will display in the terminal.  The objective is to respond with the correct order
of cards to progress through the game.

The number of cards to memorize will increment as each round completes.
In addition, the display time of the cards will decrease as each round progresses.


## Technical Overview

### Frontend

The project was limited to a terminal-based game, so images of playing cards were unfortunately out of the question.

I considered many alternatives for the card displays, but ultimately decided that creating my own text art would be the best way to approach the problem.  Using UTF-8 Characters, I was able to create the look of a regular playing card with a specified height and width.  You can see in card.py, there is a function known as card.create_cards(), which takes a list of dictionaries defining the "Type" and "Suit" of the card and returns a string.


### Backend

To enable a public scoreboard, I decided to use Amazon's Lambda Serverless Architecture.  In *lambda_function.py*, you can see everything that's going on behind the scenes.

In essense, the client communicates with the Lambda function over HTTP.  An initial request is made which creates a "Session Key", and this key is required for all further communication with the lambda function.  T
