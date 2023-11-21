import openai
from prod import ula_key
from openai import OpenAI

openai.api_key = ula_key  # type: ignore # noqa

client = OpenAI(api_key=ula_key)


class OpenAiController:
    def __init__(self) -> None:
        self.api_key = openai.api_key
        self.api_key2 = client.api_key
        self.api_url = "https://api.openai.com/v1/"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}


    def make_moderation(self, text: str) -> str:
        response = openai.Moderation.create(
            input=text
        )
        output = response["results"][0]
        print(output)
        return output

    def get_completion(self, prompt: str, system="You are a helpful assistant, your answer are no longer then 5 sentenses") -> str:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        return completion.choices[0].message.content

    def get_embedding(self, text: str) -> str:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )

        return response.data[0].embedding

    def get_whisper(self, audio_file_path) -> str:
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        return transcription.text
