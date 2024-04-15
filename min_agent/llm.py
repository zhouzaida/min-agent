import os
from typing import Optional, List

from openai import OpenAI


class LLMAPI:

    def __init__(self, model: Optional[str] = None, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.model = model or os.getenv('MODEL_NAME')
        base_url = base_url or os.getenv('BASE_URL')
        api_key = api_key or os.getenv('OPENAI_API_KEY') 

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, messages: List[dict]):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
