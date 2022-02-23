# Wordle API
<br> **Learning Objectives**
- Build a simple set of APIs in AWS to gain familiarity with AWS services
- Use Airbyte to load data into DynamoDB

<br> **AWS Architecture**
- APIs are hosted in API Gateway
- APIs call Lambda functions
- Data is stored in DynamoDB

<br> **APIs**
[newGame](https://github.com/MichaelStinson/Wordle-API/blob/main/lambda/new_game_lambda_function.py)
- Accepts end user's key as input
- Creates a new game
- Responds with corresponding game ID
[submitGuess](https://github.com/MichaelStinson/Wordle-API/blob/main/lambda/submit_guess_lambda_function.py)
- Accepts end user's key, game ID, and guess as input 
- Checks guess against the solution
- Responds with feedback on accuracy of guess and whether the puzzle has been solved

<br> **Airbyte Data Load**
- Set up a simple Airbyte connector to easily load data into DynamoDB
- Connector extracts list of Wordle solutions from a csv file and sends to DynamoDB
- The Airbyte DynamoDB stream outputs data into a staging table as a json blob 
- Each time a new item is added to the staging table, the [airbyte_tranform](https://github.com/MichaelStinson/Wordle-API/blob/main/lambda/transform_airbyte_lambda_trigger.py) Lambda function is triggered to parse the blob and update the solutions table with the new item

<br> **Screenshots from Wordle API Demo**
<br>
![Screenshot](img/screenshot1.png)
![Screenshot](img/screenshot2.png)

