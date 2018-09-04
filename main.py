# coding: utf-8
import requests
import json
import random
import card
import time
import os

URL_DB = json.load(open("urls.json"))
# Gets the urls
ALL_CARDS = json.load(open("all_cards.json"))
# Gets the list of all cards
CARD_DB = {}
for val in ALL_CARDS:
	CARD_DB[val['id_val']] = val
# Creates a map of card values
HIGH_SCORE_URL = URL_DB["highscore"]

GAME_INTRO = '''
Welcome to MemZip - the multiplayer card memorization game
(And also my KPCB project submission)

High Scores are recorded externally, so you can play against your friends!

The rules are simple - a group of randomly selected playing cards
will display in the terminal.  You have to respond with the correct order
of cards to progress through the game.

The number of cards to memorize will increment as each round completes.
To make the challenge harder, the time to look at the cards will decrease each round.

		'''


def generate_cards(count=1):
	return [random.choice(ALL_CARDS) for i in range(count)]

def convert_message(message):
	# Converts the message into a python dict
	return json.loads(message)

def get_card(id_val):
	return CARD_DB[id_val]

def display_multiple(listOfNums):
	card_info = [CARD_DB[num] for num in listOfNums]
	card_string = card.create_cards(card_info)
	print card_string


def get_high_scores():
	# Returns a python dictionary containing high scores
	res = requests.get(HIGH_SCORE_URL)
	# Makes network request to lambda function to get high score list
	return convert_message(res.json()['message'])
	# Return type is a dict

def start_new_game(username):
	url = HIGH_SCORE_URL + "?username={}&number=-1".format(username)
	res = requests.post(url)
	return res.json()

def flush_window():
	os.system('cls' if os.name == 'nt' else 'clear')
	# This will run the command to clear the terminal depending on OS
	time.sleep(.2)
	# Adding this sleep makes it look like it cleared the terminal...

class game(object):
	"""docstring for game"""
	def __init__(self, username=None, skip_intro=False):
		if skip_intro == False:
			# This means the user did not "Replay"
			self.menu()
			# Displays the menu
		else:
			self.username = username
			# Sets it the username used in the previous session
		self.highscores = get_high_scores()
		#newgame = start_new_game(self.username)
		#self.scores = newgame['order']
		self.level = 1
		# This is the level the user starts at
		self.card_order = {}
		# This is an ongoing dict keeping track of card order
		self.delay = 1
		# This is the delay between cards
		self.correct = 0
		# Correct answers by the user
		self.incorrect = 0
		# Incorrect answers by the user
		self.starting_number = 4
		# Card num is equal to level + starting num

	def menu(self):
		print(GAME_INTRO)
		# Prints the explanation of the game
		self.username = raw_input("Please enter your name to start a new game: ")
		# Grabs the username from the user
		flush_window()
		# Resets the window

	def print_countdown(self):
		# Prints the countdown before the game starts
		for i in range(3):
			print("Round #{} Starting in {}...".format(self.level, 3-i))
			time.sleep(1)
			flush_window()

	def start_game(self):
		cards_in_round = self.level + self.starting_number
		# This is the amount of cards in the round
		self.card_order[self.level] = []
		# This will reset the card order in case it's a replayed game
		self.print_countdown()
		# Prints the countdown before the game starts
		for i in range(cards_in_round):
			# Iterates over each card in round
			next_card = random.randint(1,31)
			# Picks a random card
			self.card_order[self.level].append(next_card)
			# Appends it to the current games list of cards
			display_multiple([next_card])
			# Displays the SINGLE card... not multiple cards.
			time.sleep(self.delay)
			# Sleeps for the delay specified in the beginning
			flush_window()
			# Clears the window

	def current_score_string(self):
		return "{} | Score: {} | Incorrect: {}".format(self.username, self.correct, self.incorrect)

	def submit_answers(self):
		for i in range(self.level + 5):
			correct_answer = self.card_order[self.level][i]
			card_choices = [correct_answer]
			while len(card_choices) < 4:
				temp_card = random.randint(1, 31)
				if temp_card not in card_choices:
					card_choices.append(temp_card)
			random.shuffle(card_choices)
			print self.current_score_string()
			display_multiple(card_choices)
			correct_index = card_choices.index(correct_answer)
			if int(raw_input("Input Card Number #{}: ".format(i+1))) - 1 != correct_index:
				self.incorrect += 1
			else:
				self.correct += 1
			if self.incorrect > 2:
				keep_playing = self.game_over()
				flush_window()
				return keep_playing
			flush_window()

	def print_highscore_chart(self):
		score = self.correct
		username = self.username[:15].ljust(15)
		printed = False
		screen = "{} | High Score\n\n".format('Username'.ljust(15))
		for key, value in self.highscores.items():
			if value <= score and printed == False:
				printed = True
				screen += "{} | {} (Current Player)".format(username, score) + "\n"
			screen += "{} | {}".format(key[:15].ljust(15), value)  + "\n"
		if printed == False:
			screen += "{} | {}   (Current Player)".format(username, score) + "\n"
		return screen

	def game_over(self):
		self.formatted_high_score = self.print_highscore_chart()
		flush_window()
		print "Game over :(\n\nGreat job, {}!  Here is how you stack up against the other players: \n\n{}\n\n".format(self.username, self.formatted_high_score)
		if raw_input("Play again? (Y/N) ").lower() != 'y':
			return False
		else:
			return True


if __name__ == '__main__':
	a = game()
	a.start_game()
	while a.submit_answers() == True:
		a = game(a.username, True)
		a.start_game()

