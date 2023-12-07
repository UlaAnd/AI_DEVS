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

    def get_function_calling(self):
        assistant = client.beta.assistants.create(
            instructions="'Decide whether the task should be added to the ToDo list or to the calendar (if time is provided) and return the corresponding JSON'",
            model="gpt-4-1106-preview",
            tools=[{
                "type": "function",
                "function": {
                    "name": "decizion agent",
                    "description": "Get the weather in location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                            "unit": {"type": "string", "enum": ["c", "f"]}
                        },
                        "required": ["location"]
                    }
                }
            }, {
                "type": "function",
                "function": {
                    "name": "getNickname",
                    "description": "Get the nickname of a city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                        },
                        "required": ["location"]
                    }
                }
            }]
        )

    def get_describtion(self, text, url):
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return(response.choices[0].message.content)
