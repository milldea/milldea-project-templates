import os
import boto3
import json


#
# SecretsManagerラッパークラス
#
class SecretsManager:
    @staticmethod
    def get_secret_dictionary(secret_id):
        stg = os.getenv('STAGE')
        if stg == 'local':
            # local 用なので、 secrets 情報はなんでもOK
            session = boto3.session.Session(
                aws_access_key_id='Dummy',
                aws_secret_access_key='Dummy'
            )
            client = session.client(
                service_name='secretsmanager',
                region_name='ap-northeast-1',
                endpoint_url='http://localstack:4566'
            )
            response = client.get_secret_value(
                SecretId=secret_id
            )
        else:
            client = boto3.client('secretsmanager')
            response = client.get_secret_value(
                SecretId=secret_id
            )
        return json.loads(response["SecretString"])
