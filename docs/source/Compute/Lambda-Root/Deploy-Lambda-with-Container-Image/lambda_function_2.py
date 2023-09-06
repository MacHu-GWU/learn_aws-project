# content of lambda_function_2.py

def handler_1(event, context):
    return "this is handler 1"


def handler_2(event, context):
    return "this is handler 1"


handler_mapper = dict(
    handler_1=handler_1,
    handler_2=handler_2,
)


def handler(event, context):
    func = handler_mapper[event["handler"]]
    return func(event=event["event"], context=context)
