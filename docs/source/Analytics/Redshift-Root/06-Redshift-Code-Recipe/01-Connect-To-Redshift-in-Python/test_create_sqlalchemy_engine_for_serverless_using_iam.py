# -*- coding: utf-8 -*-

"""
This example shows how to connect to Redshift Serverless using Sqlalchemy.
"""

import boto3
import uuid
import random
import textwrap
from pathlib import Path
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

import aws_redshift_helper.api as rs


Base = orm.declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id: str = sa.Column(sa.String, primary_key=True)
    create_at: str = sa.Column(sa.String)
    update_at: str = sa.Column(sa.String)
    note: str = sa.Column(sa.String, nullable=True)

    @classmethod
    def new(cls, note: str = None):
        return cls(
            id=str(uuid.uuid4()),
            create_at=datetime.utcnow().isoformat(),
            update_at=datetime.utcnow().isoformat(),
            note=note,
        )


def create_table(engine: "sa.engine.Engine"):
    with engine.connect() as conn:
        sql = textwrap.dedent(
            f"""
            DROP TABLE IF EXISTS {Transaction.__tablename__};
            """
        )
        conn.execute(sql)

    with engine.connect() as conn:
        sql = textwrap.dedent(
            f"""
            CREATE TABLE {Transaction.__tablename__}(
                id VARCHAR(36) DISTKEY NOT NULL,
                create_at VARCHAR(26) NOT NULL,
                update_at VARCHAR(26) NOT NULL,
                note VARCHAR
            )
            DISTSTYLE key
            COMPOUND SORTKEY(create_at);
            """
        )
        conn.execute(sql)


def insert_data(engine: "sa.engine.Engine"):
    print(f"Insert some data into {Transaction.__tablename__!r} table")
    with orm.Session(engine) as ses:
        transaction = Transaction.new(note=f"note {random.randint(1, 1000000)}")
        ses.add(transaction)
        ses.commit()


def select_data(engine: "sa.engine.Engine"):
    print(f"select data from {Transaction.__tablename__!r} table")

    # return object
    print("--- Return object ---")
    with orm.Session(engine) as ses:
        for transaction in ses.query(Transaction).limit(3):
            print(
                [
                    transaction.id,
                    transaction.create_at,
                    transaction.update_at,
                    transaction.note,
                ]
            )

    # return python dict
    print("--- Return dict ---")
    with engine.connect() as conn:
        for transaction in conn.execute(sa.select(Transaction).limit(3)).mappings():
            print(transaction)


# load your config
dir_here = Path(__file__).absolute().parent
path_config_serverless = dir_here / "config-serverless.json"
config_serverless = rs.Config.load(path_config_serverless)

# create boto session
boto_ses = boto3.session.Session()

# create sqlalchemy engine
engine = rs.create_sqlalchemy_engine_for_serverless_using_iam(
    boto_ses=boto_ses,
    workgroup_name=config_serverless.workgroup,
)

rs.test_engine(engine)
create_table(engine)
insert_data(engine)
select_data(engine)
