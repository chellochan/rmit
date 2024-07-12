import sys
import requests
from decimal import Decimal
import json
import io

import logging
import boto3
from botocore.exceptions import ClientError
from music import *


"""
[1] Vlad Bezden (2016. June, 14), python save image from url, available online: 
https://stackoverflow.com/questions/30229231/python-save-image-from-url
[2]: Pinolpier (2020. October, 16), raise ValueError('Fileobj must implement read'), available online:
 https://stackoverflow.com/questions/57451656/raise-valueerrorfileobj-must-implement-read
"""
def upload_file_obj(music_list, bucket):
	artist_image_dict = {}
	for song in music_list['songs']:
		artist_image_dict[song['artist']] = {
			'img_url': song['img_url'],
			'filename': img_url_to_filename(song['img_url'])
		}

	# Upload the file
	s3 = boto3.client('s3')
	try:
		for artist in artist_image_dict.keys():
			image = download_image(artist_image_dict[artist]['img_url'])
			s3.upload_fileobj(image, bucket, artist_image_dict[artist]['filename'])
	except ClientError as e:
		logging.error(e)
		return False
	return True


def download_image(url):
	file_data = requests.get(url).content
	return io.BytesIO(file_data)


if __name__ == '__main__':
	if len(sys.argv) > 2:
		file_name = sys.argv[1]
		bucket_name = sys.argv[2]
	else:
		file_name = 'a1.json'
		bucket_name = 's3939713-artist-image'
	with open(file_name) as json_file:
		music = json.load(json_file, parse_float=Decimal)
	upload_file_obj(music, bucket_name)