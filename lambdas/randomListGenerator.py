import json
import random

def lambda_handler(event, context):
    # Generate a list of 5 random integers between 1 and 100
    random_integers = [random.randint(1, 100) for _ in range(5)]
    output = {}
    output['randomList'] = random_integers
    
    return {
        'statusCode': 200,
        'body': output
    }
