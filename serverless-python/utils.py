# -*- coding:utf-8 -*-
import os
import logging
import pytz
from decimal import Decimal
from datetime import datetime

# 初期設定.
stage = "local"
if 'STAGE' in os.environ:
    stage = os.environ['STAGE']

# Logger
logger = logging.getLogger()
if stage == 'prd':
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)


class Utils:
    #
    # 現在時刻を取得(datetime)
    #
    @staticmethod
    def now():
        return datetime.now(pytz.timezone('Asia/Tokyo')).replace(microsecond=0)

    #
    # Decimal to float の型変換
    # json.dumps の default に指定
    #
    @staticmethod
    def decimal_default_proc(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError
