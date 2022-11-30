# Serverless python template

このプロジェクトは、 serverless framework で python を実行するサンプルです。
API Gateway + Lambda + DynamoDB の最小構成となっています。

## 環境準備

### Requirement

* docker-compose
* aws-cli
  * https://aws.amazon.com/jp/cli/


### ローカル環境構築

#### AWS アカウント準備

未設定人のみ、事前に設定しておく

```sh
$ aws configure
AWS Access Key ID [None]: dummy
AWS Secret Access Key [None]: dummy
Default region name [None]: 空欄のままでOK
Default output format [None]: 空欄のままでOK
```


#### Docker 起動

```sh
# コンテナを作成、起動
$ docker-compose up -d --build
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
```

```sh
$ yarn sls offline start
```

ホストマシンから curl を叩く
```
$ curl --location --request GET 'http://localhost:3000/hello'
```

以下のJSONが返ってきたらOK。
```
{
    "message": "Go Serverless v1.0! Your function executed successfully!",
    "input": .....(省略)
}
```

#### DynamoDB 確認

ホストマシンから aws cli を実行する
```sh
$ aws dynamodb list-tables --endpoint-url http://localhost:8000
```

以下の JSON が取得できれば OK。
```
{
    "TableNames": [
        "dummy-table"
    ]
}
```

その他のコマンド詳細は公式をご確認ください。
https://docs.aws.amazon.com/cli/latest/reference/dynamodb/index.html

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
  * 共通利用可能なメソッド(ビジネスロジックを含まないシンプルなもの)
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


### DynamoDB
sls offline startした時に
```
Dynamodb Local Started, Visit: http://localhost:8000/shell
```
が出力されていればOK。
seedデータとしてtest/{テーブル名}.jsonを投入しています。


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