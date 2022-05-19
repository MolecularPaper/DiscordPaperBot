# -*- coding:utf-8 -*-

import openai
from Chat import api
import re
import os


def request(text):
    if len(text) > 1500:
        return

    openai.organization = "org-O1hKvSNjES74EawZRnPeuwZ4"
    openai.api_key = "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"

    gpt = api.GPT(engine="text-davinci-002", temperature=0.4, max_tokens=100)
    output = gpt.submit_request(text).choices[0]['text'].split(':')

    special = re.compile(r'[^ A-Za-z0-9가-힣+]')
    remove_sub = special.sub("", output[len(output) - 1])
    striped = remove_sub.strip()

    return striped