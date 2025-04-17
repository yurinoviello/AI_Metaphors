import os
from typing import List

import attrs
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.chat.roles import ChatRole
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import GrazieApiGatewayClient, GrazieAgent
from grazie.api.client.llm_parameters import LLMParameters, Parameters
from grazie.api.client.profiles import LLMProfile, OpenAIo1Profile
from grazie.api.client_v2 import AuthType

from ai_metaphors.providers.assistant.llm_assistant import LlmAssistant
from ai_metaphors.utils.manim_type import ManimType


class GrazieAssistant(LlmAssistant):
    __client: GrazieApiGatewayClient
    name = "grazie-api-gateway-client-readme"
    version = "dev"

    def __init__(self, model: str, temperature: float, manim_type: ManimType):
        super().__init__(model, temperature, manim_type)
        self.__client = GrazieApiGatewayClient(
            grazie_agent=GrazieAgent(name=self.name, version=self.version),
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=os.getenv("GRAZIE_JWT_TOKEN"),
            auth_type=AuthType.USER,
        )

    def _chat_message_list(self, messages: List[LlmAssistant.Message]):
        chat = ChatPrompt()
        for message in messages:
            match (self.model, message.role):
                case (OpenAIo1Profile.name, _):
                    chat = chat.add_user(message.content)
                case (_, ChatRole.SYSTEM):
                    chat = chat.add_system(message.content)
                case _:
                    chat = chat.add_user(message.content)
        return self._safe_call(chat)

    def _safe_call(self, chat: ChatPrompt) -> str:
        @attrs.define(auto_attribs=True, frozen=True)
        class MyProfile(LLMProfile):
            name: str = self.model

        parameters: dict[Parameters.Key, Parameters.Value] = {
            LLMParameters.Temperature: Parameters.FloatValue(self.temperature),
        }

        response = self.__client.chat(
            chat=chat,
            profile=MyProfile(),
            parameters=parameters,
        ).content

        accumulated_content = ''.join(message['content'] for message in chat.get_messages())
        self.num_tokens += len(self.tokenizer.encode(accumulated_content + response))
        return response
