import os
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from google.ai.generativelanguage_v1beta.types import content


class GeminiChat:
    def __init__(self, api_key=None, model_name="gemini-2.0-flash-exp",
                 temperature=1, top_p=0.95, top_k=40, max_output_tokens=8192,
                 response_mime_type="application/json"):
        """
        Initializes the GeminiChat class with API key, model configurations and chat history.

        Args:
            api_key: Your Gemini API key. If None, uses environment variable "GEMINI_API_KEY"
            model_name (str): The name of the Gemini model to use.
            temperature (float): Controls the randomness of the response generation.
            top_p (float): Nucleus sampling parameter.
            top_k (int): Top-k sampling parameter.
            max_output_tokens (int): Maximum number of output tokens.
            response_mime_type (str): Response mime type.
        """
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key is None:
                raise ValueError("API key not provided and 'GEMINI_API_KEY' not set in environment.")
        genai.configure(api_key=api_key)

        self.generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens,
            response_schema={
                "type": "object",  # String representation of the type
                "properties": {
                    "response": {
                        "type": "boolean",  # String representation of the type
                    },
                },
            },
            response_mime_type=response_mime_type,
        )

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
        )
        self.chat_session = self.model.start_chat(history=[])

    def send_message(self, prompt):
        """
        Sends a message to the Gemini model and returns the response text.

        Args:
            prompt (str): The user message to send.

        Returns:
            str: The response text from the Gemini model.
        """
        response = self.chat_session.send_message(prompt)
        return response.text
