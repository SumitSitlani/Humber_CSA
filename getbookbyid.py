import boto3
import json
import decimal
from boto3.dynamodb.types import TypeDeserializer

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def convert_dynamodb_to_json(dynamodb_item):
    """
    Converts a DynamoDB JSON format item to a regular JSON format.
    """
    deserializer = TypeDeserializer()
    if isinstance(dynamodb_item, dict):
        return {k: convert_dynamodb_to_json(v) for k, v in dynamodb_item.items()}
    elif isinstance(dynamodb_item, list):
        return [convert_dynamodb_to_json(i) for i in dynamodb_item]
    else:
        return dynamodb_item

def lambda_handler(event, context):
    # Extract the book ID from the path parameters
    if 'pathParameters' in event and 'id' in event['pathParameters']:
        book_id = event['pathParameters']['id']
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Book ID not found in path parameters'})
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('books')

    try:
        # Retrieve the book with the specified ID
        response = table.get_item(Key={'id': int(book_id)})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'Book with ID {book_id} not found'})
            }
        
        # Convert DynamoDB JSON format to regular JSON format
        json_response = convert_dynamodb_to_json(response['Item'])

        return {
            'statusCode': 200,
            'body': json.dumps(json_response, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error retrieving book: ' + str(e)})
        }
