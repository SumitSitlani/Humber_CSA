import boto3
import json

def lambda_handler(event, context):
    # Extract the book ID from the path parameters
    if 'pathParameters' in event and 'id' in event['pathParameters']:
        book_id = event['pathParameters']['id']
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Book ID not found in path parameters'})
        }
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('books')  
    
    try:
        # Check if the book with the specified ID exists
        response = table.get_item(Key={'id': int(book_id)})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'Book with ID {book_id} does not exist'})
            }

        # Delete the item with the specified book ID
        table.delete_item(Key={'id': int(book_id)})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Book deleted successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error deleting book: ' + str(e)})
        }
