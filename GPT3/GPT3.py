# -*- coding:utf-8 -*-

import openai
from GPT3 import api
import re
import os


def request(text):
    if len(text) > 1500:
        return

    if os.path.isfile('./Data/token.txt'):
        f = open('./Data/api_key.txt')
        api_key = f.readline()
    else:
        api_key = os.environ['token']

    openai.organization = "org-O1hKvSNjES74EawZRnPeuwZ4"
    openai.api_key = api_key

    gpt = api.GPT(engine="text-davinci-002", temperature=0.4, max_tokens=100)
    output = gpt.submit_request(text).choices[0]['text'].split(':')

    special = re.compile(r'[^ A-Za-z0-9가-힣+]')
    remove_sub = special.sub("", output[len(output) - 1])
    striped = remove_sub.strip()

    return striped
