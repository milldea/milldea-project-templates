# Points

企業毎、ユーザ毎の当月のポイントを保持するテーブル


## テーブル設計

- テーブル名：Points{Stg}
- パーティションキー：CompanyId (文字列型)
- ソートキー：UserId_YM (文字列型)
  - `###` を使って文字列結合する
  - user_01###202304
- 属性：
  - UserId (文字列型)
    - UserID
  - Points (数値型)
    - 当月の獲得ポイント
  - UpdateTimestamp (数値型)
    - データを更新した日時のUnixタイムスタンプ（秒）
    - 当日の更新があったかどうかを確認するために利用する

## データアクセス

- API
  - CompanyId, UserIdのリクエストを受けて、当月の文字列（YYYYMM）を付与してクエリする
- バッチ
  - 外部 API の結果から CompanyId, UserId を取得。  
   バッチ実行時間から、 YYYYMM 文字列を生成してクエリする。
  - レコードがない場合
    - ポイント 1 で新規作成する
  - レコードがある場合
    - UpdateTimestamp が当日中の場合
      - 何もせずに終了
    - UpdateTimestamp が前日の場合
      - インクリメントして終了