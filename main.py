# coding: utf-8
import requests
import json
import random
import card
import time

URL_DB = json.load(open("urls.json"))
# Gets the urls
ALL_CARDS = json.load(open("all_cards.json"))
# Gets the list of all cards
CARD_DB = {}
for val in ALL_CARDS:
	CARD_DB[val['id_val']] = val
# Creates a map of card values
HIGH_SCORE_URL = URL_DB["highscore"]


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
	for i in range(30):
		print("")
	time.sleep(.2)

class game(object):
	"""docstring for game"""
	def __init__(self, username):
		self.menu()
		self.current_card_count = 1
		self.username = username
		#self.highscores = get_high_scores()
		#newgame = start_new_game(self.username)
		#self.scores = newgame['order']
		self.level = 0
		self.card_order = {}
		self.delay = 1

	def menu(self):
		game_menu = '''
Welcome to MemZip - the multiplayer card memorization game
(And also my KPCB project submission)

Please select a mode from the options below:

(1) Single Player Speed Round
(2) MultiPlayer (Play against the global leaderboard!)
(3) View High Scores

		'''
		print(game_menu)
		raw_input("Option: ")
		flush_window()

	def start_game(self):
		cards_in_round = self.level + 5
		# This is the amount of cards in the round
		self.card_order[self.level] = []
		for i in range(3):
			print("Round #{} Starting in {}...".format(self.level+1, 3-i))
			time.sleep(1)
			flush_window()
		for i in range(cards_in_round):
			next_card = random.randint(1,31)
			self.card_order[self.level].append(next_card)
			display_multiple([next_card])
			time.sleep(self.delay)
			flush_window()

	def submit_answers(self):
		for i in range(self.level + 5):
			correct_answer = self.card_order[self.level][i]
			card_choices = [correct_answer]
			while len(card_choices) < 4:
				temp_card = random.randint(1, 31)
				if temp_card not in card_choices:
					card_choices.append(temp_card)
			random.shuffle(card_choices)
			display_multiple(card_choices)
			correct_index = card_choices.index(correct_answer)
			if int(raw_input("Input Card Number #{}: ".format(i+1))) - 1 != correct_index:
				print("False...")
			else:
				print("True")



	def play(self, num):
		for i in range(self.current_card_count):
			card = raw_input("Next Card: ")



if __name__ == '__main__':
	#print start_new_game('test')
	#print get_high_scores()
	#print get_card(31)['image']
	#print ' '.join([a['image'] for a in generate_cards(2)])
	#for i in range(10):
	#	display_multiple([random.randint(1, 31) for i in range(1)])
	#	time.sleep(1)
	#	flush_window()
	a = game('chris')
	a.start_game()
	a.submit_answers()
