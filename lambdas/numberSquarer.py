import json

def lambda_handler(event, context):
    # Extract the input integer from the event
    input_number = int(event.get('number', None))
    

    # Calculate the square of the input integer
    result = input_number ** 2
    
    # Return the result
    return {'statusCode': 200,  'body': {'square': result}}
