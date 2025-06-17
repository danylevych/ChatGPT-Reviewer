#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import backoff
import tiktoken
from openai import OpenAI

system_prompt = '''As a tech reviewer, please provide an in-depth review of the
following pull request git diff data. Your task is to carefully analyze the title, body, and
changes made in the pull request and identify any problems that need addressing including
security issues. Please provide clear descriptions of each problem and offer constructive
suggestions for how to address them. Additionally, please consider ways to optimize the
changes made in the pull request. You should focus on providing feedback that will help
improve the quality of the codebase while also remaining concise and clear in your
explanations. Please note that unnecessary explanations or summaries should be avoided
as they may delay the review process. Your feedback should be provided in a timely
manner, using language that is easy to understand and follow.
'''


class OpenAIClient:
    '''OpenAI API client using SDK v1.0+'''

    def __init__(self, model, temperature, frequency_penalty, presence_penalty,
                 max_tokens=4000, min_tokens=256):
        self.model = model
        self.temperature = temperature
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.encoder = tiktoken.get_encoding("gpt2")

        self.is_azure = "azure" in (os.getenv("OPENAI_API_BASE") or "")
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE") or None,
        )

        self.openai_kwargs = {"model": self.model}
        if self.is_azure:
            self.openai_kwargs = {"model": self.model, "extra_headers": {"api-key": os.getenv("OPENAI_API_KEY")}}

    @backoff.on_exception(backoff.expo,
                          (Exception,),
                          max_time=300)
    def get_completion(self, prompt) -> str:
        if self.model.startswith("gpt-"):
            return self.get_completion_chat(prompt)
        else:
            return self.get_completion_text(prompt)

    def get_completion_chat(self, prompt) -> str:
        '''Invoke OpenAI API to get chat completion'''
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        stream = self.client.chat.completions.create(
            messages=messages,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            stream=True,
            max_tokens=self.max_tokens - len(self.encoder.encode(f'{system_prompt}\n{prompt}')),
            **self.openai_kwargs
        )

        completion_text = ''
        for event in stream:
            delta = event.choices[0].delta
            if delta and delta.content:
                completion_text += delta.content
        return completion_text

    def get_completion_text(self, prompt) -> str:
        '''Invoke OpenAI API to get text completion'''
        prompt_message = f'{system_prompt}\n{prompt}'

        stream = self.client.completions.create(
            prompt=prompt_message,
            temperature=self.temperature,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            stream=True,
            max_tokens=self.max_tokens - len(self.encoder.encode(prompt_message)),
            **self.openai_kwargs
        )

        completion_text = ''
        for event in stream:
            if event.choices and event.choices[0].text:
                completion_text += event.choices[0].text
        return completion_text

    def get_pr_prompt(self, title, body, changes) -> str:
        '''Generate a prompt for a PR review'''
        prompt = f'''Here are the title, body and changes for this pull request:

Title: {title}

Body: {body}

Changes:
```
{changes}
```
    '''
        return prompt

    def get_file_prompt(self, title, body, filename, changes) -> str:
        '''Generate a prompt for a file review'''
        prompt = f'''Here are the title, body and changes for this pull request:

Title: {title}

Body: {body}

And bellowing are changes for file {filename}:
```
{changes}
```
    '''
        return prompt
