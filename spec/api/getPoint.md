```mermaid
sequenceDiagram

participant APP as web app
participant API as ポイント取得API
participant COM_TABLE as (DynamoDB)<br>Company
participant HIS_TABLE as (DynamoDB)<br>Points

APP ->> API: リクエスト
note right of APP: 引数<br>- organization_id<br>- user_id
API ->> API: バリデーションチェック
opt バリデーションエラー
    API ->> API: エラー内容をログ出力(API-001)
    API ->> APP: エラーレスポンス(400)を返却
    note right of API: 処理を終了
end
API ->> COM_TABLE: organization_idのチェック(get) key:organization_id
alt 該当のorganization_idが存在しない
    API ->> API: エラー内容をログ出力(API-002)
    API ->> APP: エラーレスポンス(404)を返却
    note right of API: 処理を終了
else failure
    API ->> API: エラー内容をログ出力(API-003)
    API ->> APP: エラーレスポンス(500)を返却
    note right of API: 処理を終了
end
API ->> HIS_TABLE: ポイントレコード取得(get)<br>key: organization_id, user_yearmonth
note right of API: yearmonthは獲得時ベースとし、現在日時から生成する
API ->> API: DynamoDBレスポンス内容(Itemsの中身)をログ出力(API-004)
alt recordなし
    HIS_TABLE ->> API: record = 0
    note right of API: current_points = 0
else recordあり
    HIS_TABLE ->> API: record = 1
    note right of API: current_points = record.Points
else failure
    API ->> API: エラー内容をログ出力(API-005)
    API ->> APP: エラーレスポンス(500)を返却
    note right of API: 処理を終了
end
note right of API: earned_date = format(record.UpdateTimestamp, yyyy-mm-dd)
API ->> API: レスポンス内容をログ出力(API-006)
API ->> APP: レスポンス(200)を返却
```

# ログ仕様
| 項番      | 説明                          | ログレベル | 出力例                                                                |
|---------|-----------------------------|-------|--------------------------------------------------------------------|
| API-001 | バリデーションエラー                  | ERROR | API-001 bad request. url: {url}                                    |
| API-002 | 該当の organization_id が見つからない | ERROR | API-002 resource not found. organization_id: {organization_id}     |
| API-003 | DynamoDB アクセスに失敗            | ERROR | API-003 dynamodb request failed. request:{request}, error: {error} |
| API-004 | DynamoDB のレスポンスを出力          | INFO  | API-004 dynamodb response. request:{request}, response: {response} |
| API-005 | DynamoDB のレスポンスを出力          | ERROR  | API-005 dynamodb response. request:{request}, response: {response} |
| API-006 | 成功レスポンス                     | ERROR  | API-006 success api response. response:{response}                  |

ERROR レベルのログは stacktrace も合わせて出力する

