import os
from pathlib import Path
import attrs
from dotenv import load_dotenv
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import AuthType, GrazieAgent, GrazieApiGatewayClient
from grazie.api.client.chat.prompt import ChatPrompt
from grazie.api.client.llm_parameters import LLMParameters, Parameters
from grazie.api.client.profiles import LLMProfile
from openai import OpenAI
import tiktoken

from ai_metaphors.core.providers.prompt_provider import PromptProvider


class GrazieProvider:
    """
    GrazieProvider is a class designed to interact with the Grazie API using a specified language model.
    It facilitates generating various forms of output based on provided prompts and parameters.

    :param model: A string representing the model to be used for generating responses. Defaults to "openai-gpt-4o".
    :param temperature: A float that determines the randomness of the model's output. Defaults to 0.0.
    :param prompt_provider: An instance of PromptProvider that provides prompts for various subject types.
    """

    _client: GrazieApiGatewayClient
    _model: str
    _temperature: float
    _tokenizer: tiktoken.Encoding = tiktoken.get_encoding("cl100k_base")
    _prompt_provider: PromptProvider
    num_tokens: int = 0

    def __init__(self, model: str, temperature: float, prompt_provider: PromptProvider) -> None:
        load_dotenv()
        self._client = GrazieApiGatewayClient(
            grazie_agent=GrazieAgent(name="grazie-api-gateway-client-readme", version="dev"),
            url=GrazieApiGatewayUrls.STAGING,
            grazie_jwt_token=os.getenv("GRAZIE_JWT_TOKEN"),
            auth_type=AuthType.USER,
        )
        self._model = model
        self._temperature = temperature
        self._prompt_provider = prompt_provider

    def __safe_call(self, system_prompt: str, user_prompt: str) -> str:
        @attrs.define(auto_attribs=True, frozen=True)
        class MyProfile(LLMProfile):
            name: str = self._model

        if self._model == "openai-o1":
            return self._client.chat(
                chat=ChatPrompt().add_user(system_prompt + "\n" + user_prompt),
                profile=MyProfile(),
            ).content

        response = self._client.chat(
            chat=ChatPrompt().add_system(system_prompt).add_user(user_prompt),
            profile=MyProfile(),
            parameters={}
            if "o3" in self._model
            else {
                LLMParameters.Temperature: Parameters.FloatValue(self._temperature),
            },
        ).content

        self.num_tokens += len(self._tokenizer.encode(system_prompt + user_prompt + response))
        return response

    def change_model(self, model: str) -> None:
        self._model = model

    def get_term_definition(self) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_term_definition(),
            user_prompt=self._prompt_provider.get_user_prompt_term_definition(),
        )

    def get_one_line_term_definition(self, term_definition: str) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_one_line_term_definition(),
            user_prompt=self._prompt_provider.get_user_prompt_one_line_term_definition(term_definition),
        )

    def get_metaphor(self) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_metaphor(),
            user_prompt=self._prompt_provider.get_user_prompt_metaphor(),
        )

    def get_one_line_metaphor(self, metaphor: str) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_one_line_metaphor(),
            user_prompt=self._prompt_provider.get_user_prompt_one_line_metaphor(metaphor),
        )

    def get_classes(self, story: str, svg: str) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_classes(svg),
            user_prompt=self._prompt_provider.get_user_prompt_classes(story),
        )

    def get_description(self, story: str, one_line_story: str, classes: str) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_description(),
            user_prompt=self._prompt_provider.get_user_prompt_description(story, one_line_story, classes),
        )

    def get_manim(
        self,
        story: str,
        one_line_story: str,
        classes: str,
        svg: str,
        instructions: str,
    ) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_manim(svg),
            user_prompt=self._prompt_provider.get_user_prompt_manim(story, one_line_story, classes, instructions),
        )

    def request_static_refinement(self, code: str, runtime_error: str, static_error: str, svg: str) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_refine_manim(svg),
            user_prompt=self._prompt_provider.get_user_prompt_refine_manim(code, runtime_error, static_error),
        )

    def request_video_evaluation(self, code: str, instructions: str, images: list[str]) -> str:
        # This should be done by GrazieProvider, for now it is devoted to OPENAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        messages = [
            {
                "role": "developer",
                "content": [
                    {
                        "type": "text",
                        "text": self._prompt_provider.get_system_prompt_evaluate_video(),
                    },
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self._prompt_provider.get_user_prompt_evaluate_video(code, instructions),
                    },
                ],
            },
        ]

        for i, img in enumerate(images):
            messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Frame {i + 1}:",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img}",
                            },
                        },
                    ],
                },
            )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=3_000,
            seed=10,
        )
        return response.choices[0].message.content

    def request_video_refinement(self, instructions: str, errors_explanation: str, code: str, svg: str) -> str:
        return self.__safe_call(
            system_prompt=self._prompt_provider.get_system_prompt_fix_video(svg),
            user_prompt=self._prompt_provider.get_user_prompt_fix_video(instructions, errors_explanation, code),
        )

    @staticmethod
    def get_narration_audio(text: str, narration_audio_file: Path):
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="sage",
            input=text,
        ) as response:
            response.stream_to_file(narration_audio_file)