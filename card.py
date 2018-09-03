# coding: utf-8

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

def create_cards(height, width, cards):
	corner_left_string = "┌"
	corner_right_string = "┐"
	top_string = "─"
	right_string = "│"
	left_string = "│"
	card_template = [[] for i in range(height)]
	for card in cards:
		card_template[0].append(corner_left_string + ''.join([top_string * (width-2)]) + corner_right_string)
		card_template[1].append(create_line1(card['value'], width))
		for va in card_template:
			print str(va[0])

if __name__ == '__main__':
	create_cards(15, 15, [{"value": "10"}])

