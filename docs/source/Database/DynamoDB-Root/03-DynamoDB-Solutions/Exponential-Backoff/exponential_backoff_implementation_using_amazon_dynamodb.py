# -*- coding: utf-8 -*-

"""
This script implements the monitor lambda function with exponential backoff feature.

You can let the AWS Lambda Function to send a notification to an SNS topic
automatically when there is a failure. However, if a high concurrent Lambda Function
send tons of same failure notification to your SNS topic, it may flood your
alert system.

To avoid this, we usually use exponential backoff to ensure that we only send
small amount of notification in a short period of time.
"""

import typing as T
from datetime import datetime, timezone

import pynamodb_mate as pm


def send_notification():
    print("Just send a notification")


# reset the exponential backoff if elapsed time from the first notification
# is greater than this value
reset_time = 7 * 24 * 60 * 60  # 7 days

# the exponential backoff bracket
backoff_wait_time = [
    0,  # 0 seconds, send first notification immediately
    1 * 60,  # 1 min, wait 1 min before send the second notification
    5 * 60,  # 5 min, wait 5 min before send the third notification
    15 * 60,  # 10 min
    30 * 60,  # 30 min
    1 * 3600,  # 1 hour
    4 * 3600,  # 4 hour
    12 * 3600,  # 12 hour
    1 * 86400,  # 1 day
    2 * 86400,  # 2 day
    4 * 86400,  # 4 day
]

# backoff_wait_time = [0, 1, 5, 10, 30, 60, 300]


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


class Tracker(pm.Model):
    """
    The DynamoDB table serves as the centralized tracker for distributive workers.
    It can track the first report time and last report time to identify that
    should we send a notification or not.
    """
    class Meta:
        table_name = "notification-exponential-backoff"
        region = "us-east-1"
        billing_mode = pm.PAY_PER_REQUEST_BILLING_MODE

    # fmt: off
    pk: T.Union[str, pm.UnicodeAttribute] = pm.UnicodeAttribute(hash_key=True)
    sk: T.Union[str, pm.UnicodeAttribute] = pm.UnicodeAttribute(range_key=True)
    count: T.Union[int, pm.NumberAttribute] = pm.NumberAttribute()
    first_report_time: T.Union[datetime, pm.UTCDateTimeAttribute] = pm.UTCDateTimeAttribute()
    last_report_time: T.Union[datetime, pm.UTCDateTimeAttribute] = pm.UTCDateTimeAttribute()
    # fmt: on

    @property
    def principal_id(self) -> str:
        """
        The principal who is failed to process the task. Usually the AWS ARN.
        """
        return self.pk

    @property
    def cause_id(self) -> str:
        """
        The cause of the failure. Usually the Exception type name.
        """
        return self.sk

    @classmethod
    def send_notification(
        cls,
        principal_id: str,
        cause_id: str,
    ):
        now = get_utc_now()
        try:
            tracker = Tracker.get(principal_id, cause_id)
        except Tracker.DoesNotExist:
            tracker = Tracker(
                pk=principal_id,
                sk=cause_id,
                count=1,
                first_report_time=now,
                last_report_time=now,
            )
            send_notification()
            tracker.save()
            return tracker

        wait_time = backoff_wait_time[tracker.count]
        if (now - tracker.first_report_time).total_seconds() >= reset_time:
            send_notification()
            tracker.update(
                actions=[
                    Tracker.count.set(1),
                    Tracker.last_report_time.set(now),
                    Tracker.last_report_time.set(now),
                ]
            )
            return tracker
        elif (now - tracker.last_report_time).total_seconds() >= wait_time:
            send_notification()
            tracker.update(
                actions=[
                    Tracker.count.set(tracker.count + 1),
                    Tracker.last_report_time.set(now),
                ]
            )
            return tracker
        else:
            return None


if __name__ == "__main__":
    import time
    import moto

    mock_dynamodb = moto.mock_dynamodb()
    mock_dynamodb.start()

    pm.Connection()
    Tracker.create_table(wait=True)
    principal_id = "my-lambda-func"
    cause_id = "ValueError"

    start_time = get_utc_now()
    for _ in range(60):
        time.sleep(1)
        elapsed = int((get_utc_now() - start_time).total_seconds())
        print(f"elapsed: {elapsed}")
        tracker = Tracker.send_notification(principal_id, cause_id)
        if tracker is not None:
            print(f"  tracker: {tracker.attribute_values}")

    mock_dynamodb.stop()

    # example output:
    # elapsed: 1
    # Just send a notification
    #   tracker: {'pk': 'my-lambda-func', 'sk': 'ValueError', 'count': 1, 'first_report_time': datetime.datetime(2023, 8, 16, 14, 25, 6, 730313, tzinfo=datetime.timezone.utc), 'last_report_time': datetime.datetime(2023, 8, 16, 14, 25, 6, 730313, tzinfo=datetime.timezone.utc)}
    # elapsed: 2
    # Just send a notification
    #   tracker: {'count': 2, 'first_report_time': datetime.datetime(2023, 8, 16, 14, 25, 6, 730313, tzinfo=datetime.timezone.utc), 'last_report_time': datetime.datetime(2023, 8, 16, 14, 25, 7, 736981, tzinfo=datetime.timezone.utc), 'pk': 'my-lambda-func', 'sk': 'ValueError'}
    # elapsed: 3
    # elapsed: 4
    # elapsed: 5
    # elapsed: 6
    # elapsed: 7
    # Just send a notification
    #   tracker: {'count': 3, 'first_report_time': datetime.datetime(2023, 8, 16, 14, 25, 6, 730313, tzinfo=datetime.timezone.utc), 'last_report_time': datetime.datetime(2023, 8, 16, 14, 25, 12, 766106, tzinfo=datetime.timezone.utc), 'pk': 'my-lambda-func', 'sk': 'ValueError'}
    # elapsed: 8
    # elapsed: 9
    # elapsed: 10
    # elapsed: 11
    # elapsed: 12
    # elapsed: 13
    # elapsed: 14
    # elapsed: 15
    # elapsed: 16
    # elapsed: 17
    # Just send a notification
    #   tracker: {'count': 4, 'first_report_time': datetime.datetime(2023, 8, 16, 14, 25, 6, 730313, tzinfo=datetime.timezone.utc), 'last_report_time': datetime.datetime(2023, 8, 16, 14, 25, 22, 814980, tzinfo=datetime.timezone.utc), 'pk': 'my-lambda-func', 'sk': 'ValueError'}
    # elapsed: 18
    # elapsed: 19
    # elapsed: 20
    # elapsed: 21
    # elapsed: 22
    # elapsed: 23
    # elapsed: 24
    # elapsed: 25
    # elapsed: 26
    # elapsed: 27
    # elapsed: 28
    # elapsed: 29
    # elapsed: 30
    # elapsed: 31
    # elapsed: 32
    # elapsed: 33
    # elapsed: 34
    # elapsed: 35
    # elapsed: 36
    # elapsed: 37
    # elapsed: 38
    # elapsed: 39
    # elapsed: 40
    # elapsed: 41
    # elapsed: 42
    # elapsed: 43
    # elapsed: 44
    # elapsed: 45
    # elapsed: 46
    # elapsed: 47
    # Just send a notification
    #   tracker: {'count': 5, 'first_report_time': datetime.datetime(2023, 8, 16, 14, 25, 6, 730313, tzinfo=datetime.timezone.utc), 'last_report_time': datetime.datetime(2023, 8, 16, 14, 25, 53, 39960, tzinfo=datetime.timezone.utc), 'pk': 'my-lambda-func', 'sk': 'ValueError'}
    # elapsed: 48
    # elapsed: 49
    # elapsed: 50
    # elapsed: 51
    # elapsed: 52
    # elapsed: 53
    # elapsed: 54
    # elapsed: 55
    # elapsed: 56
    # elapsed: 57
    # elapsed: 58
    # elapsed: 59
    # elapsed: 60
