# Wordle API
<br> Learning Objectives
- Build a simple set of APIs in AWS to gain familiarity with AWS services
- Use Airbyte to load data into DynamoDB

<br> AWS Architecture
- APIs are hosted in API Gateway
- APIs call Lambda functions
- Data is stored in DynamoDB

<br> Airbyte Data Load
- Set up a simple Airbyte connector to easily load data into DynamoDB
- Connector extracts list of Wordle solutions from a csv file and sends to DynamoDB
- The Airbyte DynamoDB stream outputs data into a staging table as a json blob 
- Each time a new item is added to the staging table, the [airbyte_tranform](https://github.com/MichaelStinson/Wordle-API/blob/main/lambda/transform_airbyte_lambda_trigger.py) Lambda function is triggered to parse the blob and update the solutions table with the new item

<br> Screenshots from Wordle API Demo
![Screenshot](img/screenshot1.png)
![Screenshot](img/screenshot2.png)

