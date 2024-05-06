# -*- coding: utf-8 -*-

"""
该模块是一个非常简单的用于生成 API Key 并验证 API Key 是否过期的模块.
"""

import typing as T
import secrets
import pynamodb_mate as pm
from datetime import datetime, timedelta, timezone


T_STR = T.Union[str, pm.UnicodeAttribute]
T_DT = T.Union[datetime, pm.UTCDateTimeAttribute]


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class Auth(pm.Model):
    """
    后面的类的基类. 在 DynamoDB 中, 不同的类将会放在同一个 Table 中.
    不同类的 partition key 会有不同的前缀, 以便于查询.
    """

    pk: T_STR = pm.UnicodeAttribute(hash_key=True)


def token_to_pk(token: str) -> str:
    return f"token-{token}"


def pk_to_token(pk: str) -> str:
    return pk.split("-")[1]


class ApiToken(Auth):
    """
    代表一个用户创建的 API Token. 一个用户可以创建多个 API Token.
    """

    class Meta:
        table_name = "auth"
        region = "us-east-1"
        billing_mode = pm.PAY_PER_REQUEST_BILLING_MODE

    account_id: T_STR = pm.UnicodeAttribute()
    expire_at: T_DT = pm.UTCDateTimeAttribute()

    @property
    def token(self) -> str:
        return pk_to_token(self.pk)

    def is_expired(self, utc_now: datetime) -> bool:
        return utc_now > self.expire_at

    @classmethod
    def new(
        cls,
        account_id: str,
        expire: int,
    ):
        api_token = cls(
            pk=token_to_pk(secrets.token_hex(16)),
            account_id=account_id,
            expire_at=get_utc_now() + timedelta(seconds=expire),
        )
        api_token.save()
        return api_token

    @classmethod
    def get_if_is_allowed(cls, token: str) -> T.Optional["ApiToken"]:
        api_token = cls.get_one_or_none(token_to_pk(token))
        if api_token is None:
            return None
        if api_token.is_expired(get_utc_now()):
            return None
        else:
            return api_token


if __name__ == "__main__":
    import time
    import moto

    mock_dynamodb = moto.mock_dynamodb()
    mock_dynamodb.start()
    pm.Connection()

    ApiToken.create_table()

    account_id = "alice@email.com"
    api_token = ApiToken.new(account_id, 1)
    print(api_token.token)

    api_token_1 = ApiToken.get_if_is_allowed(api_token.token)
    print(api_token_1 is not None)

    time.sleep(2)
    api_token_1 = ApiToken.get_if_is_allowed(api_token.token)
    print(api_token_1 is not None)
