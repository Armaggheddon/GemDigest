import google.generativeai as genai

from configs import api_keys, generation_config, gemini_prompt_v2

class _GeminiHelper():
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.generation_config = generation_config

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config
        )

        # Session starts empty
        self.chat_session = self.model.start_chat()

    async def generate_text(
            self, prompt: str, history: list[str] = []
    ):
        # TODO: handle a per-user chat session
        response = await self.chat_session.send_message_async(gemini_prompt_v2 + prompt)
        return response.text
    



gemini_api = _GeminiHelper(api_keys.GEMINI_API_KEY)