# アーキテクチャ設計

## 全体構成

* Serverless Framework による CloudFormation を使ったシステム
* フロント
  * 静的コンテンツ
    * S3 に配置し、 CloudFront 経由で配信する
    ```
    Client --> CloudFront --> S3
    ```
  * API
    * JS から API Gateway を呼び出して Lambda を実行する
    ```
    Client(JavaScript) --> API Gateway --> Lambda 
    ```
* API
  * ポイントを確認する API 
    * ポイント情報以外の秘匿情報は返却しないため、認証はクエリ文字列の正当性確認のみとする
    ```
    API Gateway --> Lambda --> DynamoDB
    ```
* Batch
  * 企業単位でLambda を実行するために SQS を発行するトリガーバッチ
    * DynamoDB に登録された企業を一覧し、SQS へメッセージを送信する
    ```
    CloudWatch Events --> Lambda --> DynamoDB（企業情報取得）
                            ↓
                          SQS
    ```
  * SQS を受けて 外部 API を呼び出し集計バッチを定期実行する
    * SQS の企業コードから、ロックを確認し、 外部 API を実行する
    * 外部 API 呼び出しの結果を受けて、ユーザのポイントを加算していく
    ```
    SQS --> Lambda --> DynamoDB（ロック, 集計）
              ↓
            外部 API
    ```
* ロギング
  * 全ての Lambda は CloudWatch にログを出力する