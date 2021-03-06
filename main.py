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

SESSION_KEY = requests.get(HIGH_SCORE_URL).json()['key']

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
		# This is a non-formatted list of high scores
		self.level = 1
		# This is the level the user starts at
		self.card_order = {}
		# This is an ongoing dict keeping track of card order
		self.delay = 2
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
		for j in range(10):
			# 10 rounds total
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
			continue_game = self.submit_answers()
			# Goes to the answer submission screen
			if continue_game == False:
				# This means the user lost the game and does not want to replay
				return False
				# Returns false to exit the script
			if self.incorrect > 2:
				# Checks if the user lost the game or not
				return True
		self.game_over()
		# This means they reached the end of the game


	def current_score_string(self):
		return "{} | Score: {} | Incorrect: {}".format(self.username, self.correct, self.incorrect)

	def submit_answers(self):
		cards_in_round = self.level + self.starting_number
		# This is the amount of cards in the round
		for i in range(cards_in_round):
			# Iterates over all of the cards and asks for the order
			correct_answer = self.card_order[self.level][i]
			# This is the correct answer
			card_choices = [correct_answer]
			# Starts a list with a single element containing the correct answer
			while len(card_choices) < 4:
				# While loop until the size is > 4 - makes sure they are all unique
				temp_card = random.randint(1, 31)
				# Generates a random card id
				if temp_card not in card_choices:
					# Only appends if it's unique
					card_choices.append(temp_card)
					# Saves it to the card choices list
			random.shuffle(card_choices)
			# Shuffles the cards
			print self.current_score_string()
			# This is the header with current score information
			display_multiple(card_choices)
			# Displays all 4 cards in the terminal
			correct_index = card_choices.index(correct_answer)
			# This is the index of the correct choice | ie the right answer
			while True:
				# Loops through until the input is correct
				try:
					card_number_choice = int(raw_input("Input Card Number #{}: ".format(i+1)))
					break
				except ValueError:
					print("Invalid Input - Please enter a number between 1 and 4.")
			if int(card_number_choice) - 1 != correct_index:
				# Checks to see if it's correct or incorrect
				self.incorrect += 1
			else:
				self.correct += 1
			if self.incorrect > 2:
				# This means the person missed more than 3...
				keep_playing = self.game_over()
				# Ends game
				flush_window()
				# Clears window
				return keep_playing
				# Returns if the user wants to keep playing or not
			flush_window()
			# Clears window
		self.level += 1
		# Next level...
		if self.delay > 1:
			# Only increased if the delay is currently > 1
			self.delay -= .1
			# Decreased by .1

	def print_highscore_chart(self):
		# This is a function specifically for printing the highscore chart
		score = self.correct
		# This is the current score
		username = self.username[:15].ljust(15)
		# Gets a specified length username text
		printed = False
		# Says the user's score has not been printed yet
		screen = "{} | High Score\n\n".format('Username'.ljust(15))
		# Prints the header of the high score chart
		self.highscores = get_high_scores()
		# This repulls the new high scores
		temp_list = []
		# This will hold a list of high scores
		for key, value in self.highscores.items():
			# Iterates through all items
			temp_list.append({"name": key, "score": value})
			# Turns the dict into a list
		temp_list = sorted(temp_list, key=lambda k: int(k['score']))[::-1]
		# Creates the sorted list of high scores
		for val in temp_list:
			# Iterates through all items
			key = val['name']
			value = val['score']
			if value <= score and printed == False:
				# This means the user's score is higher than the one that's about to be printed
				screen += "{} | {} (Current Player)".format(username, score) + "\n"
				# Adds the user's score to the score list
				printed = True
				# The user's score has been printed
			screen += "{} | {}".format(key[:15].ljust(15), value)  + "\n"
			# Outputs each user in the high score list
		if printed == False:
			# This means it has not been printed
			screen += "{} | {}   (Current Player)".format(username, score) + "\n"
			# Adds the user's score to the score list
		return screen

	def game_over(self):
		# This runs when the user has 3 incorrect answers
		self.submit_high_score()
		# This submits the high score to the DB
		flush_window()
		# Clears window
		self.formatted_high_score = self.print_highscore_chart()
		# Gets a string that represents a formatted version of the high score chart
		print "Game over :(\n\nGreat job, {}!  Here is how you stack up against the other players: \n\n{}\n\n".format(self.username, self.formatted_high_score)
		# Prints out the message
		if raw_input("Play again? (Y/N) ").lower() != 'y':
			# Asks if the user wants to play again
			return False
		else:
			return True

	def submit_high_score(self):
		res = requests.post(HIGH_SCORE_URL + "?key={}&username={}&number={}".format(SESSION_KEY, self.username, self.correct))

if __name__ == '__main__':
	first_round = True
	while True:
		if first_round == True:
			a = game()
			first_round = False
		else:
			a = game(a.username, True)
		continue_game = a.start_game()
		if continue_game == False:
			exit()



