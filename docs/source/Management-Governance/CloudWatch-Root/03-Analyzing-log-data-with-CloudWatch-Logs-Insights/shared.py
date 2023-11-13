# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager
from aws_console_url.api import AWSConsole

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")
aws = AWSConsole(aws_account_id=bsm.aws_account_id, aws_region=bsm.aws_region, bsm=bsm)
logs_client = bsm.cloudwatchlogs_client

group_name = "learn_aws_cloudwatch/Analyzing-log-data-with-CloudWatch-Logs-Insights"
stream_name_1 = "container-1"
stream_name_2 = "container-2"
