import boto3


#
# SecretsManagerラッパークラス
#
class SecretsManager:
    @staticmethod
    def get_secret_binary(secret_id):
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(
            SecretId=secret_id
        )
        return response["SecretBinary"]
