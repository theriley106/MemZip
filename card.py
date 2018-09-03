# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import random
def create_line1(value, width):
	right_string = "│"
	left_string = "│"
	string = left_string
	string += value
	if value == '10':
		string += ""
	else:
		string += " "
	string += " " * (width-4)
	string += right_string
	return string

def create_line2(suit, width):
	right_string = "│"
	left_string = "│"
	string = left_string
	string += " " * ((width-3)/2)
	string += suit
	string += " " * ((width-3)/2)
	string += right_string
	return string

def create_line3(suit, value, width):
	right_string = "│"
	left_string = "│"
	string = left_string
	if value == '10':
		string += " " * ((width-6))
	else:
		string += " " * ((width-5))
	string += value
	string += " "
	string += suit
	string += right_string
	return string

def create_line4(width):
	right_string = "┘"
	left_string = "└"
	bottom_string = "─"
	string = left_string
	string += bottom_string * ((width-2))
	string += right_string
	return string

def create_cards(cards, height=10, width=15):
	corner_left_string = "┌"
	corner_right_string = "┐"
	top_string = "─"
	right_string = "│"
	left_string = "│"
	card_template = [[] for i in range(height)]
	for card in cards:
		card['suit'] = random.choice(['♠', '♦', '♥', '♣']).decode('utf-8')
		card['value'] = card['value'].decode('utf-8')
		if card['value'] != '10':
			card['value'] = str(card['value'][0])
		card_template[0].append(corner_left_string + ''.join([top_string * (width-2)]) + corner_right_string)
		card_template[1].append(create_line1(card['value'], width))
		for i in range((height-5)/2):
			string = "│"
			string += " " * (width-2)
			string += "│"
			card_template[2+i].append(string)
			at_value = 2+i
		card_template[at_value+1].append(create_line2(card['suit'], width))
		at_value = at_value + 2
		for i in range((height-5)/2):
			string = "│"
			string += " " * (width-2)
			string += "│"
			card_template[at_value+i].append(string)
			at_value = at_value+i
		card_template[at_value+1].append(create_line3(card['suit'], card['value'], width))
		card_template[at_value+2].append(create_line4(width))
	return_string = ""
	for va in card_template:
		return_string += ' '.join(va)
		return_string += "\n"
	return return_string

if __name__ == '__main__':
	create_cards(10, 15, [{"value": "K", "suit":"♥"}, {"value": "10", "suit":"♥"}, {"value": "10", "suit":"♥"}, {"value": "10", "suit":"♥"}])

