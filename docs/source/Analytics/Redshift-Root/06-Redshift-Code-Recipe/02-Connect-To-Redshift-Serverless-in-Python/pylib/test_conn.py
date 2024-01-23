# -*- coding: utf-8 -*-

import typing as T
import random


if T.TYPE_CHECKING: # pragma: no cover
    from redshift_connector import Connection
    import sqlalchemy as sa


def test_connection(conn: "Connection", verbose: bool = True):
    """
    Redshift connection.
    """
    sql = f"SELECT {random.randint(1, 100)};"
    if verbose:
        print(f"Test connection by running a query: {sql}")
    cursor = conn.cursor()
    row = cursor.execute(sql).fetchone()
    if verbose:
        print(f"Result: {row[0]}")
        print("Success!")


def test_engine(engine: "sa.engine.Engine", verbose: bool = True):
    """
    Test sqlalchemy engine.
    """
    sql = f"SELECT {random.randint(1, 100)};"
    if verbose:
        print(f"Test connection by running a query: {sql}")
    with engine.connect() as conn:
        row = conn.execute(sql).fetchone()
    if verbose:
        print(f"Result: {row[0]}")
        print("Success!")
