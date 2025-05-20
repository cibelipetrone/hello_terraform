import json

def lambda_handler(event, context):
    return success_response("Hello, Terraform!")

def success_response(message):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": message})  
    }
