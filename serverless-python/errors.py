class MyError(Exception):
    """
    自作エラー基底クラス
    """


class InvalidResourceNameError(MyError):
    """
    指定したリソース名が不正な場合に発生するエラー
    """


class QueryError(MyError):
    """
    検索時のパラメータ指定エラー
    """


class DynamoDBError(MyError):
    """
    DynamoDBアクセス時のエラー
    """


class UnknownError(MyError):
    """
    その他のエラー
    """
