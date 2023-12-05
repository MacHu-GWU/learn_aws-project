# -*- coding: utf-8 -*-

import pandas as pd
from s3pathlib import S3Path
from pyathena import connect
from prepare_data import Config, bsm

# define aws credential and s3 location
s3path_athena_result = S3Path(Config.bucket, "athena/results/")

# define connection, use AWS CLI named profile for authentication
conn = connect(
    s3_staging_dir=s3path_athena_result.uri,
    profile_name=Config.aws_profile,
    region_name=bsm.aws_region,
)

# define the SQL statement, use ${database}.${table} as t to specify the table
sql = f"""
SELECT 
    t.category,
    AVG(t.value) as average_value  
FROM {Config.glue_database}.{Config.glue_table} t
GROUP BY t.category
ORDER BY t.category
"""

# execute the SQL query, load result to pandas DataFrame
df = pd.read_sql_query(sql, conn)
print(df)
