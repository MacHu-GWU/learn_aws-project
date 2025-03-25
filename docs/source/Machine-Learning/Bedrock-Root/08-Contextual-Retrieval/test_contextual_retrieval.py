# -*- coding: utf-8 -*-

"""
Test the contextual retrieval quality of Amazon Bedrock models.

.. code-block:: bash

    pip install tiktoken

- `Prompt caching for faster model inference <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html>`_
- `BedrockRuntime.Client.converse <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html>`_
- `Invoke Amazon Nova on Amazon Bedrock using Bedrock's Converse API <https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_Converse_AmazonNovaText_section.html>`_
- `Invoke Anthropic Claude on Amazon Bedrock using the Invoke Model API <https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-runtime_example_bedrock-runtime_InvokeModel_AnthropicClaude_section.html>`_

TODO:

`prompt caching <https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html>`_
在这个 Contextual Retrieval 的 Use Case 中能降低大约 60% - 70% cost, 因为文章全文不会变, 只有 chunk 会变.
比如一个文章分 5 个 Chunk, 每个 Chunk 大约占比 20%. 那么本来 Input token 是 120, 其中 100 个 token
是文章全文.
但是目前 Prompt Caching 还在 Preview 阶段, 还没有实装,
"""

import json
import textwrap
from pathlib import Path


import tiktoken
from boto_session_manager import BotoSesManager
from rich import print as rprint

encoder = tiktoken.get_encoding("o200k_base")

aws_profile = "bmt_app_dev_us_east_1"
bsm = BotoSesManager(profile_name=aws_profile)

dir_here = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")
# inf_profile_arn = f"arn:aws:bedrock:{bsm.aws_region}:{bsm.aws_account_id}:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0"

whole_document = dir_here.joinpath("whole-document.md").read_text()
chunk = dir_here.joinpath("chunk.md").read_text()
whole_document_n_token = len(encoder.encode(whole_document))
chunk_n_token = len(encoder.encode(chunk))
prompt_template = dir_here.joinpath("prompt.md").read_text()


def test_claude_3_haiku():
    model_name = "claude_3_haiku"
    inf_profile_arn = f"arn:aws:bedrock:{bsm.aws_region}:{bsm.aws_account_id}:inference-profile/us.anthropic.claude-3-haiku-20240307-v1:0"

    prompt = prompt_template.format(WHOLE_DOCUMENT=whole_document)
    chunk_message = f"<chunk>\n{chunk}\n</chunk>"
    messages = [
        {
            "role": "user",
            "content": [
                {"text": prompt},
                {"text": chunk_message},
            ],
        },
    ]
    response = bsm.bedrockruntime_client.converse(
        modelId=inf_profile_arn,
        messages=messages,
        inferenceConfig={"maxTokens": 300, "temperature": 0.5, "topP": 0.9},
    )
    response.pop("ResponseMetadata")
    dir_tmp.joinpath(f"{model_name}.json").write_text(json.dumps(response, indent=4))

    context = response["output"]["message"]["content"][0]["text"]
    dir_tmp.joinpath(f"{model_name}.md").write_text(context)


def test_amazon_nova_micro():
    model_name = "amazon_nova_micro_1_0"
    inf_profile_arn = f"arn:aws:bedrock:{bsm.aws_region}:{bsm.aws_account_id}:inference-profile/us.amazon.nova-micro-v1:0"

    prompt = prompt_template.format(WHOLE_DOCUMENT=whole_document)
    chunk_message = f"<chunk>\n{chunk}\n</chunk>"
    messages = [
        {
            "role": "user",
            "content": [
                {"text": prompt},
                {"text": chunk_message},
            ],
        },
    ]
    response = bsm.bedrockruntime_client.converse(
        modelId=inf_profile_arn,
        messages=messages,
        inferenceConfig={"maxTokens": 300, "temperature": 0.5, "topP": 0.9},
    )
    response.pop("ResponseMetadata")
    path = dir_tmp.joinpath(f"{model_name}.json")
    path.write_text(json.dumps(response, indent=4))

    context = response["output"]["message"]["content"][0]["text"]
    dir_tmp.joinpath(f"{model_name}.md").write_text(context)


if __name__ == "__main__":
    """
    """
    # test_claude_3_haiku()
    # test_amazon_nova_micro()
