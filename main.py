import requests
import json

URL_DB = json.load(open("urls.json"))

HIGH_SCORE_URL = URL_DB["highscore"]

def get_high_scores():
	return

if __name__ == '__main__':
	print HIGH_SCORE_URL
