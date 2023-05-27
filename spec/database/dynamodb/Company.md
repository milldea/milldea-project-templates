# Company

企業毎の 外部 API Key とロック情報を保持するテーブル

## テーブル設計

- テーブル名：Company{Stg}
- パーティションキー：CompanyId (文字列型)
  - 企業ID
- 属性：
  - CompanyName (文字列型)
    - 企業名
  - ApiKey (文字列型)
    - 外部 API Key
  - UpdateAt (数値型)
    - ロック獲得時の current_timestamp + 固定時間の値をセット

## データアクセス

- トリガーバッチ
  - 全ての企業情報を取得するため、スキャンして全件取得する
  - UpdateAt が未設定の場合は、 SQS にメッセージを流す
- 集計バッチ
  - 企業IDを Key に UpdateAt を更新する
