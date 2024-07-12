import boto3


def create_movie_table(dynamodb=None):
	if not dynamodb:
		# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
		dynamodb = boto3.resource('dynamodb')

	''' [1] RMIT School of Computing Technologies, 
	COSC2640 Cloud Computing, Lab sheet - Exercise 4 - AWS Database Services (Python).pdf
	'''
	table = dynamodb.create_table(
		TableName='music',
		KeySchema=[
			{
				'AttributeName': 'title',
				'KeyType': 'HASH' # Partition key
			},
			{
				'AttributeName': 'artist',
				'KeyType': 'RANGE' # Sort key
			}
		],
		AttributeDefinitions=[
			{
				'AttributeName': 'title',
				'AttributeType': 'S'
			},
			{
				'AttributeName': 'artist',
				'AttributeType': 'S'
			},
		 ],
		ProvisionedThroughput={
			'ReadCapacityUnits': 10,
			'WriteCapacityUnits': 10
		}
	)
	return table


if __name__ == '__main__':
	movie_table = create_movie_table()
	print("Table status:", movie_table.table_status)