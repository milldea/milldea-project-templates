import os
import boto3


#
# DynamoDBラッパークラス
#
class DynamoDB:
    def __init__(self, event):
        stg = os.getenv('STAGE')
        if stg == 'local':
            self.res = boto3.resource('dynamodb',
                                      aws_access_key_id="dummy",
                                      aws_secret_access_key="dummy",
                                      endpoint_url="http://localstack:4566")
        else:
            self.res = boto3.resource('dynamodb',
                                      endpoint_url=None)

    def sample_table(self):
        return self.res.Table(os.environ['DYNAMO_DB_TABLE_NAME'])
