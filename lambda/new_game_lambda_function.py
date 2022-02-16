import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
import uuid
from time import gmtime, strftime

# create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')
# use the DynamoDB object to select our table
solution_table = dynamodb.Table('solutions')
game_table = dynamodb.Table('games')
key_table = dynamodb.Table('keys')

# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
    # extract values from the event object we got from the Lambda service and store in a variable
    key = event['key']

    # Check that key is valid
    try:
        response = key_table.get_item(Key={'key':key})
        response['Item']
        #print(response)
    except:
        return {
        'statusCode': 401,
        'body': {'description': "Unauthorized"}
    }

    # Select a solution for the new game
    #TODO Add an optional parameter in event to receive a soluton ID (for testing or running thru specific set of solutions to solve)
    #TODO Add an optional paramter for daily puzzle, in order to return the same solution to all users for a given date
    
    # If no optional parameters specified, pick  a random solution from the list of solutions
    rand_id = str(uuid.uuid4())
    found = False
    
    while not found:
        response = solution_table.scan(
            Limit=1,
            ExclusiveStartKey={
                'solution_id': rand_id
            }
        )
        if response['Count'] == 1:
            found = True
    
    solution_id = response['Items'][0]['solution_id']
    solution = response['Items'][0]['solution']

    # Generate a game_id
    game_id = str(uuid.uuid4())
    
    # Get the current time
    now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    # Init empty arrs for guesses and checks    
    guesses = []
    checks = []
    
    # Save the new game details
    game_table.put_item(
            Item={
                'game_id': game_id,
                'key': key,
                'solution_id': solution_id,
                'game_won': False,
                'start_time' : now,
                'guesses' : guesses,
                'checks' : checks
                })
    
    return {
        'statusCode': 200,
        'body': {
            'game_id': game_id
        }
    }