# coding: utf-8
import requests
import json
import random
import card

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

def display_multiple(listOfNums, per_line_count=4):
	card_info = [CARD_DB[num] for num in listOfNums]
	print card.create_cards(card_info)


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

class game(object):
	"""docstring for game"""
	def __init__(self, username):
		self.current_card_count = 1
		self.username = username
		self.highscores = get_high_scores()
		newgame = start_new_game(self.username)
		self.scores = newgame['order']

	def play(self, num):
		for i in range(self.current_card_count):
			card = raw_input("Next Card: ")



if __name__ == '__main__':
	#print start_new_game('test')
	#print get_high_scores()
	#print get_card(31)['image']
	#print ' '.join([a['image'] for a in generate_cards(2)])
	display_multiple([31])
