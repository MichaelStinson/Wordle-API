import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from time import gmtime, strftime

# Create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')

# Select relevant tables
solution_table = dynamodb.Table('solutions')
game_table = dynamodb.Table('games')
key_table = dynamodb.Table('keys')
dictionary_table = dynamodb.Table('dictionary')

def lambda_handler(event, context):
    key = event['key']
    game_id = event['game_id']
    guess = event['guess'].upper()

    # Check that game_id is not null in API call
    if game_id == "":
        return set_response(200, "", "", "", "", "No Game ID provided")

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
    
    # Get data for current game, based on game_id
    try:
        response = game_table.get_item(Key={'game_id':game_id})
        response['Item']
    except:
        return set_response(200, game_id, "", "", "",  "Game ID not found")
    
    game_won = response['Item']['game_won']
    guesses = response['Item']['guesses']
    checks = response['Item']['checks']
    solution_id = response['Item']['solution_id']
    start_time = response['Item']['start_time']
    
    # Check that submitted key and game's key match, or return error
    if not (key == response['Item']['key']):
        return set_response(200, game_id, game_won, guesses, checks, "Game ID not found")
    
    # Check is game has already been won or too many guesses have already been taken
    # If either is true, return appropriate response
    if game_won:
        return game_over(200, game_id, game_won, guesses, checks, "Game has already been won", solution_id)
    
    if len(guesses) > 5:
        return game_over(200, game_id, game_won, guesses, checks, "Game is already over", solution_id)
    
    # Check that guess exists in dictionary
    try:
        err = dictionary_table.get_item(Key={'word':guess})
        err['Item']
    except:
        #print(e)#print(guess)
        return set_response(200, game_id, game_won, guesses, checks,  "Invalid guess. Try again")
    
    guess_check = compare(guess, get_solution(solution_id))
    
    if guess_check == -1:
        return set_response(200, game_id, game_won, guesses, checks, "Invalid guess. Try again")
    
    guesses.append(guess)
    checks.append(guess_check)
    
    print(guesses)
    
    if ("0" in guess_check) or ("2" in guess_check):
        if len(guesses) < 6:
            r = set_response (200, game_id, game_won, guesses, checks, "Try another guess")
        else:
            r = game_over(200, game_id, game_won, guesses, checks, "Game over!", solution_id)
    else:
        game_won = True
        r = game_over(200, game_id, game_won, guesses, checks, "Correct!", solution_id)
    
    game_table.put_item(
            Item={
                'game_id': game_id,
                'solution_id': solution_id,
                'game_won': game_won,
                'start_time' : start_time,
                'guesses' : guesses,
                "checks" : checks,
                'key':key
                })

    return r

def set_response(statusCode, game_id, game_won, guesses, checks, desc):
    return {
        'statusCode': statusCode,
        'body': {
            'game_id': game_id,
            'game_won': game_won,
            'guesses': guesses,
            'checks': checks,
            'descrtipion': desc
            }
        }

def game_over(statusCode, game_id, game_won, guesses, checks, desc, solution_id):
    return {
        'statusCode': statusCode,
        'body': {
            'game_id': game_id,
            'game_won': game_won,
            'solution': get_solution(solution_id),
            'guesses': guesses,
            'checks': checks,
            'descrtipion': desc
            }
        }
    
def get_solution(solution_id):
    r = solution_table.get_item(Key={'solution_id':solution_id})
    return r['Item']['solution']
    
def compare (g, s):
    # If guess and solution are not the same length, return an error
    if len(g) != len(s):
        return -1
    
    # Check each character in the guess against the solution
    # If the right character is in the right location, represent with a 1
    # If the right character is in the wrong location, represent with a 2
    # If the character does not exist in the solution, represent with a 0
    ret = ""
    for element in range(0, len(s)):
        if g[element] == s[element]:
            ret += "1"
        elif g[element] in s:
            ret += "2"
        else:
            ret += "0"
    
    return ret