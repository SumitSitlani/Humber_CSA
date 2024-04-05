import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('books')

    
    body = event
    
    
    book_id = body['id']
    title = body['Title']
    authors = body['Authors']
    publisher = body['Publisher']
    year = body['Year']

    
    response = table.get_item(
        Key={
            'id': book_id
        }
    )
    
    
    if 'Item' in response:
        return {
            'statusCode': 400,
            'body': json.dumps('Book ID already exists')
        }

    
    table.put_item(
        Item={
            'id': book_id,
            'Title': title,
            'Authors': authors,
            'Publisher': publisher,
            'Year': year
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Book added successfully')
    }
