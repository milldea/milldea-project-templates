import os


class Const:
    # *serverless.ymlで使わない
    # *シークレットの類でない
    # *ランタイムで変更しない
    # 定数
    def __init__(self):
        stg = os.getenv('STAGE')
        if stg == 'local':
            self.ENV_VALUE = "local"
        elif stg == 'dev':
            self.ENV_VALUE = "dev"
        elif stg == 'stg':
            self.ENV_VALUE = "stg"
        elif stg == 'prd':
            self.ENV_VALUE = "prd"
