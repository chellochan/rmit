from boto3.dynamodb.conditions import Key, Attr
from music import get_music_by_title_list

user_attr_music= 'subscribed_music_list'


def login_check(email, password, dynamodb):
	if not dynamodb:
		raise Exception('no db defined')

	table = dynamodb.Table('login')

	response = table.query(
		KeyConditionExpression=Key('email').eq(email),
		FilterExpression=Attr("password").eq(password)
	)
	return response['Count'] > 0


def register_check(email, dynamodb):
	if not dynamodb:
		raise Exception('no db defined')

	table = dynamodb.Table('login')

	response = table.query(
		KeyConditionExpression=Key('email').eq(email)
	)
	return response['Count'] == 0


def register_acc(email, username, password, dynamodb):
	if not dynamodb:
		raise Exception('no db defined')

	table = dynamodb.Table('login')

	response = table.put_item(Item={
		'email': email,
		'user_name': username,
		'password': password
	})

	return response


def load_user_detail(email, dynamodb):
	if not dynamodb:
		raise Exception('no db defined')

	login_table = dynamodb.Table('login')
	# music_table = dynamodb.Table('music')

	response = login_table.query(
		KeyConditionExpression=Key('email').eq(email)
	)
	user = response['Items'][0]
	username = user['user_name']

	subscribed_music_list = []
	# check user has subscribed music
	if 'subscribed_music_list' in user:
		subscribed_music_title_list = user['subscribed_music_list']
		subscribed_music_list = get_music_by_title_list(subscribed_music_title_list, dynamodb)

	return {
		'email': email,
		'username': username,
		'music_list': subscribed_music_list
	}


def get_user_by_email(email, dynamodb):
	if not dynamodb:
		raise Exception('no db defined')

	table = dynamodb.Table('login')

	response = table.query(
		KeyConditionExpression=Key('email').eq(email)
	)
	if response['Count'] > 0:
		user = response['Items'][0]
	else:
		user = None
	return user


def music_subscribe(title, email, dynamodb):
	if not dynamodb:
		raise Exception('no db defined')

	table = dynamodb.Table('login')

	user = get_user_by_email(email, dynamodb)
	if 'subscribed_music_list' in user:
		response = table.update_item(
			Key={
				'email': email
			},
			UpdateExpression="SET #attrName = list_append(#attrName, :attrValue)",
			ExpressionAttributeNames={
				'#attrName': 'subscribed_music_list'
			},
			ExpressionAttributeValues={
				':attrValue': [title]
			}
		)
	else:
		response = table.update_item(
			Key={
				'email': email
			},
			UpdateExpression="set #attrName = :attrValue",
			ExpressionAttributeNames = {
				'#attrName': 'subscribed_music_list'
			},
			ExpressionAttributeValues={
				':attrValue': [title]
			},
			ReturnValues="UPDATED_NEW"
		)

	return response


def music_remove_subscribe(title, email, dynamodb):
	if not dynamodb:
		raise Exception('no db defined')

	table = dynamodb.Table('login')

	user = get_user_by_email(email, dynamodb)

	idx = user[user_attr_music].index(title)
	if idx >= 0:
		update_str = 'remove subscribed_music_list[:n]'.replace(':n', str(idx))
		response = table.update_item(
			Key={'email': email},
			UpdateExpression=update_str,
			ReturnValues="UPDATED_NEW"
		)
	return response


# import boto3
# if __name__ == '__main__':
# 	dynamodb = boto3.resource('dynamodb')
#
# 	# print(login_check('s393971@student.rmit.edu.au', '012345', dynamodb))
# 	# print(register_acc('test@student.rmit.edu.au', 'edit', 'abc123', dynamodb))
# 	# music_subscribe('Folsom Prison Blues', 's39397130@student.rmit.edu.au', dynamodb)
# 	music_remove_subscribe('Folsom Prison Blues', 's39397130@student.rmit.edu.au', dynamodb)