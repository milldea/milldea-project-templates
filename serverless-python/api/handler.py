import json
from library.aws.secrets_manager import SecretsManager
from library.aws.dynamodb import DynamoDB


def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def setup_dynamodb(event, context):
    sample_table = DynamoDB(event).sample_table()
    sample_id = "00001"
    sample_name = "milldea_test"
    item = {
        "user_id": sample_id,
        "user_name": sample_name,
        "other": "sample",
    }
    sample_table.put_item(Item=item)
    response_item = sample_table.get_item(
            Key={
                "user_id": sample_id,
                "user_name": sample_name
            }
        )
    response = {
        "statusCode": 200,
        "body": response_item["Item"]
    }
    return response


def get_secrets(event, context):
    body = {
        "secret": SecretsManager.get_secret_dictionary("local-key")
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
