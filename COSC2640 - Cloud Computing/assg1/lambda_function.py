import boto3


def lambda_handler(event: any, context):
	dynamodb = boto3.resource("dynamodb")

	action = event["action"]
	table_name = event["table_name"]
	payload = event["payload"]

	all_table_names = list(map(lambda t: t.name, list(dynamodb.tables.all())))

	if table_name in all_table_names:
		table = dynamodb.Table(table_name)

		if action == "read":
			try:
				response = table.get_item(Key=payload)
				if 'Item' in response:
					item = response['Item']
				else:
					item = f'No item found in {table_name}. payload: {payload}'
			except:
				item = f'Reading: Payload(key) error in {table_name}. payload: {payload}'
		elif action == "update":
			payload = event["payload"]
			response = table.put_item(Item=payload, ReturnValues="ALL_OLD")
			item = response
		else:
			item = f'action({action}) not support'
		return item
	else:
		return f'Table name ({table_name}) invalid'


if __name__ == "__main__":
	result = lambda_handler(event={
		'action': 'update',
		'table_name': 'login',
		'payload': {
			'email': 'z',
			'password': 'edited2'
		}
	})
	print(result)
