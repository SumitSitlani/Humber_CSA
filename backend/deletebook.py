import boto3
import json

def lambda_handler(event, context):
    
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
        
        response = table.get_item(Key={'id': int(book_id)})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'Book with ID {book_id} does not exist'})
            }

        
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
