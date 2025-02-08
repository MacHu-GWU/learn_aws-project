# -*- coding: utf-8 -*-

import json

from rich import print as rprint

from osmpoc.obj import bsm

bd = bsm.get_client("bedrock-runtime")

prompt = """
Introduce yourself with in 100 words
""".strip()
body = {
    "anthropic_version": "bedrock-2023-05-31",
    "anthropic_beta": ["computer-use-2024-10-22"],
    "max_tokens": 300,
    "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    "temperature": 0.1,
    "top_p": 0.9,
}
res = bd.invoke_model(
    body=json.dumps(body),
    accept="application/json",
    contentType="application/json",
    modelId="arn:aws:bedrock:us-east-1:510022808362:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0",
)
rprint(json.loads(res["body"].read().decode("utf-8")))
"""
{
    'id': 'msg_bdrk_01MbrKB7sBT5MvjtJZe4FeEP',
    'type': 'message',
    'role': 'assistant',
    'model': 'claude-3-5-haiku-20241022',
    'content': [
        {
            'type': 'text',
            'text': "Hi there! I'm Claude, an AI created by Anthropic to be 
helpful, honest, and harmless. I aim to assist you with a wide range of tasks 
like writing, analysis, problem-solving, and answering questions. I have strong 
language and reasoning capabilities, but I'm always direct about being an AI. I 
won't pretend to be human or have feelings I don't actually experience. My goal 
is to provide accurate, ethical, and thoughtful support while being transparent 
about my nature. I enjoy engaging in substantive conversations and helping 
people effectively. I'm curious to learn and eager to help you with whatever you
need."
        }
    ],
    'stop_reason': 'end_turn',
    'stop_sequence': None,
    'usage': {'input_tokens': 16, 'output_tokens': 135}
}
"""
