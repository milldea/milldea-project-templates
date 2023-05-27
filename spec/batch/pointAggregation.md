# メインフロー

```mermaid
sequenceDiagram

participant SQS as SQS
participant AGGREGATION as (Lambda)<br>集計バッチ
participant COM_TABLE as (DynamoDB)<br>Company
participant POINT_TABLE as (DynamoDB)<br>Points
participant API as API

SQS ->>+ AGGREGATION: 起動
note right of SQS: 引数<br>- CompanyId<br>- ApiKey
AGGREGATION ->> AGGREGATION: 集計開始ログ出力(AGGREGATION-001)
AGGREGATION ->> COM_TABLE: ロック確認(get)<br>key: CompanyId
opt DynamoDB エラー
    AGGREGATION ->> AGGREGATION: エラー内容をログ出力(AGGREGATION-002)
    note right of AGGREGATION: 処理を終了
end
AGGREGATION ->> AGGREGATION: レスポンスログ出力(AGGREGATION-003)
note right of AGGREGATION: now = now()
alt item.UpdateAt exists
    note right of AGGREGATION: expiration = item.UpdateAt + 120 minutes
    alt expiration < now
        AGGREGATION ->> AGGREGATION: 長時間ロックエラーログ出力(AGGREGATION-004)
    else Locked
        AGGREGATION ->> AGGREGATION: ロック中ログ出力(AGGREGATION-005)
        note right of AGGREGATION: 処理を終了
    end
end
AGGREGATION ->> COM_TABLE: ロック獲得(put)
note right of AGGREGATION: key: CompanyId<br>UpdateAt=now
opt DynamoDB エラー
    AGGREGATION ->> AGGREGATION: エラー内容をログ出力(AGGREGATION-006)
    note right of AGGREGATION: 処理を終了
end
note right of AGGREGATION: signature と timestamp をApiKeyから生成
AGGREGATION ->> API: 外部 API
note right of AGGREGATION: 引数<br>-signature=signature<br>-timestamp=timestamp<br>-company_id=CompanyId
opt API API エラー
    AGGREGATION ->> AGGREGATION: エラー内容をログ出力(AGGREGATION-007)
    note right of AGGREGATION: [ロック解除]
    note right of AGGREGATION: 処理を終了
end
AGGREGATION ->> AGGREGATION: レスポンスログ出力(AGGREGATION-008)

note right of AGGREGATION: start_of_day = 当日 0:00 のタイムスタンプを生成
loop user in response.users
    alt user.event_timestamp == null
        AGGREGATION ->> AGGREGATION: 未検知ユーザ出力(AGGREGATION-009)
        note right of AGGREGATION: continue (過去に一度も検知したことがないユーザ)
    else user.event_timestamp < start_of_day
        AGGREGATION ->> AGGREGATION: 当日未検知ユーザ出力(AGGREGATION-010)
        note right of AGGREGATION: continue (当日の検知がないため)
    end
    AGGREGATION ->> POINT_TABLE: put_item<key>: CompanyId, user_number+yyyymm
    note right of AGGREGATION: ConditionExpression=<br>attribute_not_exists(CompanyId) and UpdateTimestamp < :day_start
    note right of AGGREGATION: UpdateExpression=<br>SET Points = if_not_exists(Points, :initVal) + :incrementVal, UpdateTimestamp = now

    opt DynamoDB エラー
        AGGREGATION ->> AGGREGATION: エラー内容をログ出力(AGGREGATION-011)
        note right of AGGREGATION: continue
    end
end
note right of AGGREGATION: [ロック解除]
AGGREGATION ->> AGGREGATION: 集計終了ログ出力(AGGREGATION-012)
```

# ロック解除

```mermaid
sequenceDiagram

participant AGGREGATION as (Lambda)<br>集計バッチ
participant COM_TABLE as (DynamoDB)<br>Company
AGGREGATION ->> COM_TABLE: ロック削除(update_item)<br>key: CompanyId
opt DynamoDB エラー
    AGGREGATION ->> AGGREGATION: エラー内容をログ出力(AGGREGATION-002)
    note right of AGGREGATION: 処理を終了
end
```

# ログ仕様
| 項番             | 説明                              | ログレベル | 出力例                                                      |
|------------------|---------------------------------|-----------|----------------------------------------------------------|
| AGGREGATION-001  | 集計開始ログ                     | Info      | AGGREGATION-001 AGGREGATION Batch start.                  |
| AGGREGATION-002  | DynamoDB アクセス失敗            | Error     | AGGREGATION-002 failed to access DynamoDB. error: {error} |
| AGGREGATION-003  | DynamoDB レスポンス表示           | Info      | AGGREGATION-003 dynamodb response. response: {response}   |
| AGGREGATION-004  | レコードが長期間ロックしているため、ロックを削除する | Error     | AGGREGATION-004 record locked too long. item:{item}       |
| AGGREGATION-005  | レコードがロックされている          | Info      | AGGREGATION-005 locked record. item:{item}                |
| AGGREGATION-006  | DynamoDB アクセス失敗            | Error     | AGGREGATION-006 failed to access DynamoDB. request:{request}, error: {error} |
| AGGREGATION-007  | API API アクセス失敗             | Error     | AGGREGATION-007 failed to access API API. request:{request}, error: {error} |
| AGGREGATION-008  | API API レスポンス                 | Info      | AGGREGATION-008 success API API. request:{request}, error: {error} |
| AGGREGATION-009  | event_timestamp が null           | Info      | AGGREGATION-009 event_timestamp is null. user:{user}      |
| AGGREGATION-010  | event_timestamp が 昨日以前        | Info      | AGGREGATION-010 event_timestamp is older than yesterday. user:{user} |
| AGGREGATION-011  | DynamoDB アクセス失敗            | Error     | AGGREGATION-011 failed to access DynamoDB. request:{request}, error: {error} |
| AGGREGATION-012  | 集計終了ログ                     | Info      | AGGREGATION-012 AGGREGATION Batch end.                    |
| AGGREGATION-999  | 原因不明のエラー                  | Error     | AGGREGATION-999 Unknown error.                            |

ERROR レベルのログは stacktrace も合わせて出力する


