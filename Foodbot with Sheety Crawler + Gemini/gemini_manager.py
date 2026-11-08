from google import genai
from google.genai import types
import os
# from dotenv import load_dotenv
# load_dotenv()

default_model_list = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash"]
GEMINI_API_KEY= os.environ.get("GEMINI_API_KEY")

class GeminiManager:

    def __init__(self, timeout_ms: int, initial_delay: int, attempts: int, models: list[str] = None):
        self._api_key = GEMINI_API_KEY
        self._models = models or default_model_list
        self._initial_delay = initial_delay
        self._attempts = attempts
        self._client = genai.Client(
            api_key=self._api_key,
            http_options=types.HttpOptions(
                timeout=timeout_ms,
                retry_options=types.HttpRetryOptions(
                    initial_delay=self._initial_delay,
                    attempts=self._attempts,
                    http_status_codes=[429, 500, 502, 503, 504],
                )
            ),
        )

    def generate_response(self, prompt):
        return self._generate_with_fallback(prompt)

    def _generate_with_fallback(self, prompt: str) -> str:
        for model in self._models:
            try:
                print(f"Trying {model}")
                interaction = self._client.interactions.create(
                    model=model,
                    input=prompt
                )
                completion = interaction.output_text
                print(f"Successfully generated response with {model}")
                print(completion)
                return completion
            except Exception as e:
                print(f"Failed with {model}: {e}")
                continue

        raise RuntimeError("All configured Gemini models failed to generate a response.")
