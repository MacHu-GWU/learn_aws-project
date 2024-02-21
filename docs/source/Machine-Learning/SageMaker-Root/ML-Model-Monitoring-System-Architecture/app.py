# -*- coding: utf-8 -*-

from model_monitoring.api import logger


logger.sink.enable_cloudwatch_logs()

@logger.capture_request()
def fn_inference(input: dict) -> dict:
    return ...


"""
-- A sample query to find slow inference transactions
-- model = /abc_corp/claim/doc_classification
-- time range = (24 hours ago, now)
SELECT
    *,
    json_extract(message, '$.elapse') AS elapse,
FROM model_monitoring_logs t
WHERE
    t.model_name = 'document_classification'
    AND t.measurement_type = 'inference_transaction'
    AND t.start_at >= '2023-01-01T00:00:00.000Z' 
    AND t.start_at <= '2023-01-02T00:00:00.000Z'
    AND t.elapse >= 3000
ORDER BY t.start_at DESC
LIMIT 20;
"""

_ = {
    "namespace": "/abc_corp/claim",
    "model_name": "doc_classification",
    "model_version": 1,
    "description": "this version improves here and there, so that ...",
    "artifacts": [
        {
            "name": "trained",
            "uri": "s3://abc_corp/claim/doc_classification/trained/1.tar.gz",
        },
        {
            "name": "static_data",
            "uri": "s3://abc_corp/claim/doc_classification/static_data/1.tar.gz",
        }
    ],
    "create_at": "2023-01-01T00:00:00.000Z",
    "created_by": "arn:aws:iam::123456789012:user/alice",
}