# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone

from rich import print as rprint

from recipe import run_query, reformat_query_results
from shared import logs_client, group_name

now = datetime.utcnow().replace(tzinfo=timezone.utc)
five_minutes_ago = now - timedelta(minutes=5)

query = """
fields @timestamp, @message, @logStream, @log
| sort @timestamp desc
""".strip()

query_id, res = run_query(
    logs_client,
    log_group_name=group_name,
    start_datetime=five_minutes_ago,
    end_datetime=now,
    query=query,
    limit=20,
)
print(f"query_id = {query_id}")
# res = logs_client.get_query_results(queryId="a1b2c3d4") # use this for a known query id
records = reformat_query_results(res)
print("records =")
rprint(records)
print(f"total records = {len(records)}")
