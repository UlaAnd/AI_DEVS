import openai
from prod import ula_key


openai.api_key = ula_key  # type: ignore # noqa


class OpenAiController:
    def __init__(self) -> None:
        self.api_key = openai.api_key
        self.api_url = "https://api.openai.com/v1/"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def make_moderation(self, text: str) -> str:
        response = openai.Moderation.create(
            input=text
        )
        output = response["results"][0]
        print(output)
        return output

    def get_completion(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant, your answer are no longer then 5 sentenses"},
            {"role": "user", "content": prompt},
        ]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=100, temperature=0.5
        )

        return completion.choices[0].message["content"]
