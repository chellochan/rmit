from boto3.dynamodb.conditions import Key, Attr
import boto3
import logging
from botocore.exceptions import ClientError

s3_bucket_name = 's3939713-artist-image'
s3_expiration = 300

def get_music_by_title_list(title_list, dynamodb):
	table = dynamodb.Table('music')

	music_list = []
	for sub_music_title in title_list:
		response_music = table.query(
			KeyConditionExpression=Key('title').eq(sub_music_title)
		)
		music_list.append(response_music['Items'][0])
	for music in music_list:
		music['s3_url'] = get_image_from_s3_by_img_url(music['img_url'])
	return music_list


def music_query(title, year, artist, dynamodb):
	if not dynamodb:
		raise Exception('no db defined')

	table = dynamodb.Table('music')

	condition = Key('title').begins_with('')
	if title is not None:
		condition = condition & Key('title').eq(title)
	if year is not None:
		condition = condition & Attr('year').eq(year)
	if artist is not None:
		condition = condition & Attr('artist').eq(artist)

	response = table.scan(
		FilterExpression=condition
	)
	if response['Count'] > 0:
		return response['Items']
	else:
		return None


def get_image_from_s3_by_img_url(img_url):
	return get_image_from_s3_by_file_key(img_url_to_filename(img_url))


def get_image_from_s3_by_file_key(file_key):
	s3_client = boto3.client('s3')
	try:
		response = s3_client.generate_presigned_url('get_object',
													Params={'Bucket': s3_bucket_name,
															'Key': file_key},
													ExpiresIn=s3_expiration)
		return response
	except ClientError as e:
		logging.error(e)
		return None


def img_url_to_filename(img_url):
	return img_url[img_url.rindex('/') + 1:]


# import boto3
if __name__ == '__main__':
	dynamodb = boto3.resource('dynamodb')

	# login_check('s39397130@student.rmit.edu.au', '012345', dynamodb)
	# print(register_acc('test@student.rmit.edu.au', 'edit', 'abc123', dynamodb))
	# print(music_query(None, '1977', None, dynamodb))
	img_url = 'https://raw.githubusercontent.com/davidpots/songnotes_cms/master/public/images/artists/JohnLennon.jpg'
	img_url2 = 'https://raw.githubusercontent.com/davidpots/songnotes_cms/master/public/images/artists/Train.jpg'
	print(get_image_from_s3_by_img_url(img_url2))

