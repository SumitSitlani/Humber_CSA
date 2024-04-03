import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('books')

    # Parse the event directly as a JSON object
    body = event
    
    # Extract book attributes from the JSON object
    book_id = body['id']
    title = body['Title']
    authors = body['Authors']
    publisher = body['Publisher']
    year = body['Year']

    # Check if the book ID already exists in the table
    response = table.get_item(
        Key={
            'id': book_id
        }
    )
    
    # If the item already exists, return an error
    if 'Item' in response:
        return {
            'statusCode': 400,
            'body': json.dumps('Book ID already exists')
        }

    # If the item does not exist, add the book to the table
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
