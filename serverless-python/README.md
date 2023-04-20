# Serverless python template

このプロジェクトは、 serverless framework で python を実行するサンプルです。
API Gateway + Lambda を serverless-framework で実行する最小構成となっています。

また、 localstack により、dynamodb, s3, secretsmanager などの各種サービスも同時に起動します。

本テンプレートではdynamoDB, secretsmanager へアクセスするライブラリのサンプルも付けています。

## 環境準備

### Requirement

* docker-compose
* aws-cli
  * https://aws.amazon.com/jp/cli/


### ローカル環境構築

#### AWS アカウント準備

ホストマシンから AWS CLI を実行する場合はホストマシンで以下の設定しておく

```sh
$ aws configure
AWS Access Key ID [None]: dummy
AWS Secret Access Key [None]: dummy
Default region name [None]: ap-northeast-1
Default output format [None]: json
```


#### Docker 起動

```sh
# コンテナを作成、起動
$ docker-compose up -d --build
```

#### LocalStack のステータス確認

```sh
$ curl localhost:4566/_localstack/health | jq
{
  "features": {
    "initScripts": "initialized"
  },
  "services": {
    "acm": "available",
    "apigateway": "available",
    "cloudformation": "available",
    "cloudwatch": "available",
    "config": "available",
    "dynamodb": "available",
    "dynamodbstreams": "available",
    "ec2": "available",
    "es": "available",
    "events": "available",
    "firehose": "available",
    "iam": "available",
    "kinesis": "available",
    "kms": "available",
    "lambda": "available",
    "logs": "available",
    "opensearch": "available",
    "redshift": "available",
    "resource-groups": "available",
    "resourcegroupstaggingapi": "available",
    "route53": "available",
    "route53resolver": "available",
    "s3": "available",
    "s3control": "available",
    "secretsmanager": "available",
    "ses": "available",
    "sns": "available",
    "sqs": "available",
    "ssm": "available",
    "stepfunctions": "available",
    "sts": "available",
    "support": "available",
    "swf": "available",
    "transcribe": "available"
  },
  "version": "1.1.1.dev"
}
```

#### localstack のログを確認

ホストマシンから実行する
```sh
$ docker-compose logs -f localstack
```

#### Docker 接続

```sh
# 作成したコンテナに接続
$ docker-compose exec sls bash --login
```

#### API 起動

コンテナ内で以下のコマンド実行

```sh
# 初回は必ず実行する
$ sh init.sh

# コンテナ内で AWS CLI を実行する場合はコンテナ内で以下の設定しておく
$ aws configure
AWS Access Key ID [None]: dummy
AWS Secret Access Key [None]: dummy
Default region name [None]: ap-northeast-1
Default output format [None]: json
```


```sh
$ sls offline start
```

ホストマシンから curl を叩く
```
$ curl --location --request GET 'http://localhost:3000/local/hello'
```

以下のJSONが返ってきたらOK。
```
{
    "message": "Go Serverless v1.0! Your function executed successfully!",
    "input": .....(省略)
}
```

#### DynamoDB 準備

##### テーブルの作成

コマンドで実行する場合
```sh
$ awslocal dynamodb create-table --table-name sample --attribute-definitions \
        AttributeName=user_id,AttributeType=S \
        AttributeName=user_name,AttributeType=S \
    --key-schema AttributeName=user_id,KeyType=HASH \
     AttributeName=user_name,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
```

serverless framework で localstack にデプロイする場合(localstack pro版を使っていない場合、非推奨)
```sh
$ sls deploy
```

##### テーブルの構築確認

ホストマシンから aws cli を実行する
```sh
$ aws --endpoint-url http://localhost:4566 dynamodb list-tables 
```

コンテナ内から実行する場合
```sh
$ awslocal dynamodb list-tables 
```


以下の JSON が取得できれば OK。
```
{
    "TableNames": [
        "local"
    ]
}
```

##### レコードの登録と確認

```sh
$ sls invoke local -f setup_dynamodb

```

その他のコマンド詳細は公式をご確認ください。
https://docs.aws.amazon.com/cli/latest/reference/dynamodb/index.html

#### SecretsManager 準備

##### Key の登録
適当な json ファイルを用意
```sh
$ echo "{\"hoge\": \"fuga\"}" >> key.json
```


ホストマシンから secrets manager を登録する場合
```sh
$ aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name local-key --secret-string file://key.json
```

コンテナ内から実行する場合
```sh
$ awslocal secretsmanager create-secret --name local-key --secret-string file://key.json
```

Binary で登録したい場合は --secret-binary で可能です。
詳しくは公式をご確認ください。
https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/create-secret.html


##### Key の作成確認

コンテナ内で以下を実行する
```sh
$ sls invoke local -f get_secrets
{
    "statusCode": 200,
    "body": "{\"secret\": {\"hoge\": \"fuga\"}}"
}
```


#### Docker 終了

```sh
$ docker-compose stop
# または
$ docker-compose down
```

down すると setup した内容が消えるので注意


## ディレクトリ構造

* api                
  * 各種APIソース
    * API Gateway または ALB 経由の handler を格納
* conf
  * env
    * 各環境向けの環境変数を定義
  * provider
    * iam Role を定義
  * resources
    * DynamoDB や S3 など、プロジェクトで必要な resource を定義
* library
  * 外部ライブラリをラップしたものなど
* spec
  * 設計ファイルを格納する
  * API は openapi で定義
  * フローは mermaid で定義
* test_data
  * ローカルテスト用のデータなど
* tests
  * pytest用のテストファイル、テスト設定など
* const.py
  * 以下の条件を満たす定数を格納する
    * serverless.ymlで使わない
    * シークレットの類でない
    * ランタイムで変更しない
* utils.py
  * 共通利用可能なメソッド(ロギングやタイムスタンプ変換などシンプルなもの)
* errors.py
  * 自前のException定義
* docker-compose.yml
  * ローカル開発環境の定義
* serverless.yml
  * serverless framework の主定義
  * https://www.serverless.com/

## デプロイ

```sh
# 全リソースをデプロイする場合
$ sls --aws-profile {your profile} deploy --stage={stage}
# 関数のみをデプロイする場合
$ sls --aws-profile {your profile} deploy function --f hogeFunc --stage={stage}
```
## コード規約

black, isort, flake8を導入済み。   
レビュー依頼前に全て手元で実行する。
### Formatter
コンテナ内で
```
isort . 
black . 
```
実行で自動整形/インポート並び替えをしてくれる。
(blackとisortの整形方法に競合する箇所があるため、isort→blackの順で実行する。)

### Linter
```
flake8 -v
```
エラーが出た場合は解消する。    
ignoreしたいエラーやexcludeしたいディレクトリが出てきた時は```.flake8```を適宜編集する

## 開発中の注意点

### docker について

Docker のベースイメージは、 Lambda と合わせて AL2 とする
https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/runtimes-images.html#runtimes-images-lp

### python モジュールの追加

新しい python モジュールを追加した場合は、以下のコマンドでバージョンを固定すること。

```sh
pip freeze > requirements.txt
```

### ディレクトリの追加

中身が空の（空じゃない場合、実行される） `__init__.py` を作成しておく。
作成しないとモジュールとして認識されず、実行時にエラーが発生する。

### env

環境変数はサイズ制限があるため、可能な限り、 const.py に記載する

### Secret 情報

AWS Secrets Manager を使うこと


### Tips
各種エディタにblackなど各ツールのプラグインがあり、設定すると便利。   
例 VS Codeの場合 (本PJディレクトリ/.vscode/settings.json)
```
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
      }
}
```
↑本PJディレクトリ配下のみ、Pythonファイル保存時にblackを使用した自動整形がかかる設定


## テンプレート環境構築メモ

https://www.serverless.com/framework/docs/getting-started

```sh
$ npm install -g serverless
$ serverless
$ cd serverless-python
# serverless.yml を適宜修正
$ serverless plugin install -n serverless-python-requirements
# これをすると、 package.json が生成される
$ serverless plugin install -n serverless-offline
$ serverless plugin install -n serverless-dynamodb-local
```

### M1 Mac の話
pyenv install は Rosetta を使うと失敗する。

### Docker ファイルの話

* 複数ポート解放する書き方
  * EXPOSE 3000 8000

### docker-compose.yml の話

volumes でプロジェクトルートをしている
Dockerfile でファイルを作成しても、 volumes の内容で上書きされる
（.node-version, .python-version, .anyenv あたりは消えてしまうので注意）

### init.sh の話

初回起動時のコマンドが増えてきて面倒だったので、init.sh にしています