import json
import random
import os

DATABASE_FILE_LOCATION = "tmp/data.json"

if os.path.exists(DATABASE_FILE_LOCATION) == False:
    # The file doesn't exist
    with open(DATABASE_FILE_LOCATION, 'w') as outfile:
        json.dump({}, outfile)
    # Create the file

DATABASE = json.load(open(DATABASE_FILE_LOCATION))

TEMP_DB = {}
RANDOM_CARDS = [random.randint(0,9) for i in range(1000)]

def gen_random_number():
    return random.randint(000000, 999999)

def respond(continue_game, message="", highscore=False):
    # This is the format of the returned HTTP response
    body_message = {'continue': continue_game, 'message': message, 'high_score': highscore}
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
    if int(num) == -1:
        # This means it is a new game
        TEMP_DB[username] = {'score': 0, 'order': [random.randint(0,9) for i in range(1000)]}
        return respond(True, message = TEMP_DB[username])
    else:
        if username in TEMP_DB:
            # It won't continue unless the username is in the temp_db to prevent cheating
            if len(TEMP_DB[username]['order']) == 0:
                # This means the person went through all of the items...
                if username in DATABASE:
                    # This means the username exists in the main DB already
                    if TEMP_DB[username]['score'] > DATABASE[username]:
                        # This means the score is higher than the previous
                        save_to_db(username, TEMP_DB[username]['score'])
                        # Saves it to the main DB
                else:
                    # This means the name doesn't exist in the high score DB yet
                    save_to_db(username, TEMP_DB[username]['score'])
                    # Saves it to the main DB
                return respond(False, "End of game... you already reached 1000")
                # This tells the client to stop the game
            if TEMP_DB[username]['order'].pop(0) == num:
                # Grabs the next card
                TEMP_DB[username]['score'] += 1
                # Adds a point to the score
                return respond(True)
                # Continues the game
            else:
                highscore = True
                # This means it was the wrong answer
                if username in DATABASE:
                    # If the username is in the main DB
                    if TEMP_DB[username]['score'] > DATABASE[username]:
                        # This means the score is higher than the previous
                        save_to_db(username, TEMP_DB[username]['score'])
                        # Saves it to the main DB
                    else:
                        highscore = False
                else:
                    # This means the name doesn't exist in the high score DB yet
                    save_to_db(username, TEMP_DB[username]['score'])
                    # Saves it to the main DB
                return respond(False, "Wrong answer :(", highscore)

def save_to_db(username, score):
    DATABASE[username] = score
    with open(DATABASE_FILE_LOCATION, 'w') as outfile:
        json.dump(DATABASE, outfile)

def return_error():
    error_message = "Invalid Request"
    return response(error_message)

def lambda_handler(event, context):
    type_of_request = event['httpMethod']
    if type_of_request == "POST":
        payload = event['queryStringParameters']
        if 'username' in payload and 'number' in payload:
            return update(payload['username'], payload['num'])
        else:
            return respond(False, message=str(payload))
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
