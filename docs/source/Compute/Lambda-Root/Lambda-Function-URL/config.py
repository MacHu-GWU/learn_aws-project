# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager

url = "https://qwkvw2wk76qcrueuwivyjhsbli0pfmbo.lambda-url.us-east-1.on.aws"
bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")

url_id = url.replace("https://", "").split(".")[0]
