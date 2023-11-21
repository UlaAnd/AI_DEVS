import requests
import prod


class ControllerApi:
    def __init__(self) -> None:
        self.dev_key = prod.api_key_devs

    def get_auth(self, task_name: str):
        url = f'https://zadania.aidevs.pl/token/{task_name}'
        params = {'apikey': self.dev_key}
        try:
            response = requests.post(url, json=params)
            response.raise_for_status()
            data = response.json()
            print(data)
            return data.get("token")

        except requests.exceptions.RequestException as e:
            print("Błąd:", e)

    def get_task(self, token):
        url = f"https://zadania.aidevs.pl/task/{token}"
        try:
            response = requests.post(url)
            response.raise_for_status()
            data = response.json()
            print(data)
            return data
        except requests.exceptions.RequestException as e:
            print("Błąd:", e)

    def post_answer(self, token, task_answer):
        url = f"https://zadania.aidevs.pl/answer/{token}"
        params = {"answer": task_answer}
        try:
            response = requests.post(url, json=params)
            response.raise_for_status()
            data = response.json()
            print(data)
            return data
        except requests.exceptions.RequestException as e:
            print("Błąd:", e)
