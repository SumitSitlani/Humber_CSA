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
    deserializer = TypeDeserializer()
    if isinstance(dynamodb_item, dict):
        return {k: convert_dynamodb_to_json(v) for k, v in dynamodb_item.items()}
    elif isinstance(dynamodb_item, list):
        return [convert_dynamodb_to_json(i) for i in dynamodb_item]
    else:
        return dynamodb_item

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('books')

    response = table.scan()


    json_response = [convert_dynamodb_to_json(item) for item in response['Items']]

    return {
        'statusCode': 200,
        'body': json_response
    }
