import os
import anthropic
from src.config import ANTHROPIC_API_KEY

class ClaudeClient:
    def __init__(self):
        self.api_key = ANTHROPIC_API_KEY
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def complete(self, prompt: str, model: str = "claude-3-sonnet-20240229", max_tokens: int = 1024) -> str:
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text if response.content else "" 