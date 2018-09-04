import json
import random
import os
import datetime
import re

DATABASE_FILE_LOCATION = "/tmp/data.json"
KEY_DB_LOCATION = "/tmp/keys.json"

if os.path.exists(DATABASE_FILE_LOCATION) == False:
	# The file doesn't exist
	with open(DATABASE_FILE_LOCATION, 'w') as outfile:
		json.dump({}, outfile)
	# Create the file

if os.path.exists(KEY_DB_LOCATION) == False:
	# The file doesn't exist
	with open(KEY_DB_LOCATION, 'w') as outfile:
		json.dump([], outfile)
	# Create the file

DATABASE = json.load(open(DATABASE_FILE_LOCATION))

TEMP_DB = {}
RANDOM_CARDS = [random.randint(0,9) for i in range(1000)]

def get_utc_time():
	return (now - datetime.datetime(1970, 1, 1)).total_seconds()

def gen_random_number(length=15):
	return [str(random.randint(0,9)) for i in range(length)]

def respond(continue_game, message="", highscore=False):
	# This is the format of the returned HTTP response
	body_message = {'continue': continue_game, 'message': message, 'high_score': highscore}
	body_message['key'] = create_new_key()
	response = {
		'statusCode': '200',
		'body': json.dumps(body_message),
		'headers': {
			'Content-Type': 'application/json',
		},
	}
	print response
	return response

def currentHighScores():
	return open(DATABASE_FILE_LOCATION).read()

def update(username, num):
	if username in DATABASE:
		# This means the username exists in the main DB already
		if num > DATABASE[username]:
			# This means the score is higher than the previous
			save_to_db(username, num)
			# Saves it to the main DB
	else:
		# This means the name doesn't exist in the high score DB yet
		save_to_db(username, num)
		# Saves it to the main DB
	return respond(True, message="AYY THIS WORKS")

def save_to_db(username, score):
	print("Adding: {} | {}".format(username, score))
	DATABASE[username] = score
	with open(DATABASE_FILE_LOCATION, 'w') as outfile:
		json.dump(DATABASE, outfile)
	print json.load(open(DATABASE_FILE_LOCATION))

def remove_from_db(username):
	del DATABASE[username]
	with open(DATABASE_FILE_LOCATION, 'w') as outfile:
		json.dump(DATABASE, outfile)
	print json.load(open(DATABASE_FILE_LOCATION))

def create_new_key():
	key = ''.join(gen_random_number())
	keys = read_keys()
	keys.append(key)
	with open(KEY_DB_LOCATION, 'w') as outfile:
		json.dump(keys, outfile)
	return key

def read_keys():
	return json.load(open(KEY_DB_LOCATION))

def is_key(key):
	return (key in re.findall('\d+', str(read_keys())))

def return_error():
	error_message = "Invalid Request"
	return response(error_message)

def lambda_handler(event, context):
	type_of_request = event['httpMethod']
	if type_of_request == "POST":
		payload = event['queryStringParameters']
		if 'key' in payload:
			if is_key(payload['key']) == True:
				if 'username' in payload and 'number' in payload:
					return update(payload['username'], payload['number'])
				else:
					return respond(False, message=str(payload))
			elif payload['key'] == open("master_key.txt").read().strip():
				# This means I am logging in with the master key
				try:
					remove_from_db(payload['username'])
					return respond(False, "Removed {}".format(payload['username']))
				except:
					return respond(False, message="Problem with master key")
			else:
				return respond(False, message="Invalid Key")
		else:
			return respond(False, message="No Params")
	else:
		message = currentHighScores()
		print("Returning high scores")
		return respond(False, message=message)

if __name__ == '__main__':
	# This means it is run directly, which I mainly did for testing
	update('chriss', -1)
	for i in range(30):
		update('chriss', RANDOM_CARDS[0])
	update('chriss', 11)
