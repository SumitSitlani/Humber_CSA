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

    if 'body' in event:
        try:
            updated_book_data = json.loads(event['body'])
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid request body format'})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Request body not found'})
        }
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('books')  
    
    try:
        
        response = table.get_item(Key={'id': int(book_id)})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f'Book with ID {book_id} does not exist'})
            }
        
        # Update the item with the specified book ID
        update_expression = 'SET Authors = :authors, Publisher = :publisher, Title = :title'
        expression_attribute_values = {
            ':authors': updated_book_data.get('Authors', response['Item']['Authors']),
            ':publisher': updated_book_data.get('Publisher', response['Item']['Publisher']),
            ':title': updated_book_data.get('Title', response['Item']['Title'])
        }
        
        
        if 'Year' in updated_book_data:
            update_expression += ', #yr = :year'
            expression_attribute_values[':year'] = updated_book_data['Year']
            expression_attribute_names = {'#yr': 'Year'}
        else:
            expression_attribute_names = None
        
        
        table.update_item(
            Key={'id': int(book_id)},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Book updated successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error updating book: ' + str(e)})
        }
