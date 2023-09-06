# -*- coding: utf-8 -*-

import typing as T
import uuid
from datetime import datetime, timedelta, timezone
import pynamodb_mate as pm
from boto_session_manager import BotoSesManager

# ------------------------------------------------------------------------------
# Server Side Logic
# ------------------------------------------------------------------------------

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
with bsm.awscli():
    # import os
    # for k, v in os.environ.items():
    #     if k.startswith("AWS"):
    #         print(k, v)

    pm.Connection()


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class Account(pm.Model):
    class Meta:
        table_name = "auth_server"
        region = bsm.aws_region
        billing_mode = pm.PAY_PER_REQUEST_BILLING_MODE

    id = pm.UnicodeAttribute(hash_key=True)
    password = pm.UnicodeAttribute()

    @property
    def email(self) -> str:
        return self.id

    @classmethod
    def new(
        cls,
        email: str,
        password: str,
    ) -> "Account":
        return cls(
            id=email,
            password=password,
        )

    def gen_api_key(self) -> "ApiKey":
        return ApiKey.new(
            access_key="access_key-" + uuid.uuid4().hex,
            secret_key="secret_key-" + uuid.uuid4().hex,
            email=self.email,
        )


class ApiKey(pm.Model):
    class Meta:
        table_name = "auth_server"
        region = bsm.aws_region
        billing_mode = pm.PAY_PER_REQUEST_BILLING_MODE

    id = pm.UnicodeAttribute(hash_key=True)
    secret_key = pm.UnicodeAttribute()
    token = pm.UnicodeAttribute(null=True)
    expire_at = pm.UTCDateTimeAttribute(null=True)
    email = pm.UnicodeAttribute()

    @property
    def access_key(self) -> str:
        return self.id

    @classmethod
    def new(
        cls,
        access_key: str,
        secret_key: str,
        email: str,
    ) -> "ApiKey":
        return cls(
            id=access_key,
            secret_key=secret_key,
            email=email,
        )

    def authorize(self):
        token = "token-" + uuid.uuid4().hex
        now = get_utc_now()
        expire_at = now + timedelta(minutes=15)
        self.token = token
        self.expire_at = expire_at
        self.update(
            actions=[
                ApiKey.token.set(token),
                ApiKey.expire_at.set(expire_at),
            ]
        )


Account.create_table(wait=True)
print(Account.get_table_items_console_url())


# ------------------------------------------------------------------------------
# Client Side Logic
# ------------------------------------------------------------------------------
email = "alice@example.com"
password = "123456"

account = Account.get_one_or_none(email)
if account is None:
    account = Account.new(email, password)
    account.save()
print(account.to_dict())

access_key = "access_key-2f6a3a73e7e942e59a884b0fb9b88fef"

api_key = ApiKey.get(access_key)
if api_key is None:
    api_key = account.gen_api_key()
    api_key.save()
print(api_key.to_dict())

api_key.authorize()
print(api_key.to_dict())
