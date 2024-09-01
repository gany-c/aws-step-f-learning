import json

def lambda_handler(event, context):
    # Extract the list of numbers in string format from the event
    numbers_str = event.get('squares', [])  # Default to an empty list string if not provided
    
    try:
        # Parse the string into a list of integers
        numbers = [int(num) for num in numbers_str]
    except (ValueError, json.JSONDecodeError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input format. Please provide a valid JSON array of numbers.'})
        }
    
    # Calculate the sum of the numbers
    total_sum = sum(numbers)
    
    # Return the sum in the response
    return {
        'statusCode': 200,
        'body': {'sum': total_sum}
    }
