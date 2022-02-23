### Trigger that runs every time a new solution is added to the airbyte_solutions staging table
### Extracts the solution and creates a new entry in the solutions table

import json
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a DynamoDB object using the AWS SDK
dynamodb = boto3.resource('dynamodb')

# Select relevant tables
solution_table = dynamodb.Table('solutions')

def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] == "INSERT" or record['eventName'] == "MODIFY": 
            logger.info(record)
            logger.info(record['dynamodb']['NewImage']['_airbyte_data']['M']['solution_id']['S'])
            
            _airbyte_ab_id = record['dynamodb']['NewImage']['_airbyte_ab_id']['S']
            solution = record['dynamodb']['NewImage']['_airbyte_data']['M']['solution_id']['S'].upper()
            
            solution_table.put_item(
                Item={
                    'solution_id': _airbyte_ab_id,
                    'solution': solution
                    })
        
        elif record['eventName'] == "REMOVE":
            logger.info(record)
            
            _airbyte_ab_id = record['dynamodb']['Keys']['_airbyte_ab_id']['S']
            
            solution_table.delete_item(
                Key={
                    'solution_id': _airbyte_ab_id
                    })

    return True
