import os
from typing import List
from openai import OpenAI

from ai_metaphors.providers.assistant.llm_assistant import LlmAssistant, ContentType
from ai_metaphors.utils.manim_type import ManimType


class OpenAIAssistant(LlmAssistant):
    client: OpenAI

    def __init__(self, model: str, temperature: float, manim_type: ManimType):
        super().__init__(model, temperature, manim_type)
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def _chat_message_list(self, messages: List[LlmAssistant.Message]) -> str:
        chat = []
        for message in messages:
            if message.content_type == ContentType.TEXT:
                chat.append({
                    "role": message.role.value,
                    "content": message.content
                })
            elif message.content_type == ContentType.IMAGE:
                chat.append({
                    "role": message.role.value,
                    "content": [{
                        "type": "image_url",
                        "image_url": {
                            "url": message.content
                        }
                    }]
                })
            else:
                raise RuntimeError(f"Unsupported content type {message.content_type}")

        return self._safe_call(chat)

    def _safe_call(self, chat: List[dict]) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=chat,
            max_tokens=3_000,
            seed=10,
        )
        return response.choices[0].message.content
