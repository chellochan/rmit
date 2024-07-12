from decimal import Decimal
import json
import boto3


def load_music(music, dynamodb=None):
	if not dynamodb:
		# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
		dynamodb = boto3.resource('dynamodb')
	''' [1] RMIT School of Computing Technologies, 
	COSC2640 Cloud Computing, Lab sheet - Exercise 4 - AWS Database Services (Python).pdf
	'''
	table = dynamodb.Table('music')
	songs = music['songs']
	for song in songs:
		title = song['title']
		artist = song['artist']
		print("Adding song:", title, artist)
		table.put_item(Item=song)


if __name__ == '__main__':
	with open("a1.json") as json_file:
		music = json.load(json_file, parse_float=Decimal)
	load_music(music)
