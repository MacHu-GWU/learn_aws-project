# -*- coding: utf-8 -*-

import json
import dataclasses
from datetime import datetime

from boto_session_manager import BotoSesManager


@dataclasses.dataclass
class Experiment:
    bsm: BotoSesManager
    rule_name: str
    lbd_func_name: str

    def create_eventbridge_rule_and_target(self):
        """
        使用 boto3 创建 EventBridge 规则并配置 Lambda 目标
        """
        try:
            # 1. 创建 EventBridge 规则
            print("创建 EventBridge 规则...")

            # 定义事件模式 - 匹配我们发送的事件
            event_pattern = {
                "source": ["my.application"],
                "detail-type": ["User Action"],
            }

            rule_response = self.bsm.eventbridge_client.put_rule(
                Name=self.rule_name,
                EventPattern=json.dumps(event_pattern),  # 事件模式，用于匹配事件
                State="ENABLED",  # 规则状态：ENABLED 或 DISABLED
                Description="Rule to trigger Lambda function from EventBridge events",
                EventBusName="default",  # 可选：指定事件总线，默认为 'default'
            )

            rule_arn = rule_response["RuleArn"]
            print(f"规则创建成功: {rule_arn}")

            # 2. 添加 Lambda 函数作为目标
            print("添加 Lambda 目标...")

            lambda_arn = f"arn:aws:lambda:{self.bsm.aws_region}:{self.bsm.aws_account_id}:function:{self.lbd_func_name}"

            targets_response = self.bsm.eventbridge_client.put_targets(
                Rule=self.rule_name,
                EventBusName="default",  # 可选：指定事件总线
                Targets=[
                    {
                        "Id": "1",  # 目标 ID，在规则内必须唯一
                        "Arn": lambda_arn,  # Lambda 函数的 ARN
                        # 可选：输入转换器，用于修改传递给目标的事件格式
                        # 'InputTransformer': {
                        #     'InputPathsMap': {
                        #         'id': '$.detail.input.id'
                        #     },
                        #     'InputTemplate': '{"user_id": "<id>"}'
                        # }
                    }
                ],
            )

            print("Lambda 目标添加成功")

            # 3. 给 EventBridge 权限调用 Lambda 函数
            print("设置 Lambda 权限...")

            try:
                self.bsm.lambda_client.add_permission(
                    FunctionName=self.lbd_func_name,
                    StatementId="eventbridge-invoke-permission",  # 权限语句 ID
                    Action="lambda:InvokeFunction",
                    Principal="events.amazonaws.com",
                    SourceArn=rule_arn,  # 允许这个特定规则调用 Lambda
                )
                print("Lambda 权限设置成功")

            except self.bsm.lambda_client.exceptions.ResourceConflictException:
                print("Lambda 权限已存在，跳过设置")

            print("\n=== 配置完成 ===")
            print(f"规则名称: {self.rule_name}")
            print(f"规则 ARN: {rule_arn}")
            print(f"Lambda 函数: {self.lbd_func_name}")
            print(f"事件模式: {json.dumps(event_pattern, indent=2)}")

            return rule_arn

        except Exception as e:
            print(f"创建规则失败: {str(e)}")
            return None

    def send_event_to_eventbridge(self):
        event_payload = {"input": {"id": 1}}
        try:
            # 发送事件到 EventBridge
            response = self.bsm.eventbridge_client.put_events(
                Entries=[
                    {
                        "Source": "my.application",  # 事件源
                        "DetailType": "User Action",  # 事件类型描述
                        "Detail": json.dumps(
                            event_payload
                        ),  # 事件详细内容，必须是 JSON 字符串
                        "EventBusName": "default",  # 使用默认事件总线，也可以创建自定义事件总线
                        "Time": datetime.now(),  # 事件时间戳
                    }
                ]
            )

            print("事件发送成功:")
            print(f"事件ID: {response['Entries'][0]['EventId']}")
            print(f"发送的事件内容: {json.dumps(event_payload, indent=2)}")

        except Exception as e:
            print(f"发送事件失败: {str(e)}")


if __name__ == "__main__":
    exp = Experiment(
        bsm=BotoSesManager(
            profile_name="bmt_app_dev_us_east_1",
            region_name="us-east-1",
        ),
        rule_name="TriggerTheLearnEventBridgeLambdaFunction",
        lbd_func_name="learn_event_bridge",
    )
    bsm = exp.bsm
    # exp.create_eventbridge_rule_and_target()
    # exp.send_event_to_eventbridge()
