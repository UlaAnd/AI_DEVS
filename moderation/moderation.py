
import requests

import prod
from controller import OpenAiController


def get_auth(task_name="moderation", key=prod.api_key_devs):
    url = f'https://zadania.aidevs.pl/token/{task_name}'
    params = {'apikey': key}
    try:
        response = requests.post(url, json=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data.get("token")

    except requests.exceptions.RequestException as e:
        print("Błąd:", e)


def get_task():
    token = get_auth()
    url = f"https://zadania.aidevs.pl/task/{token}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
        return [data.get("input"), token]
    except requests.exceptions.RequestException as e:
        print("Błąd:", e)


def post_answer():
    task = get_task()
    texts = task[0]
    url = f"https://zadania.aidevs.pl/answer/{task[1]}"
    answer = []
    for text in texts:
        controller = OpenAiController()
        result = controller.make_moderation(text=text)
        if result.get("flagged"):
            answer.append(1)
        else:
            answer.append(0)
    params = {"answer": answer}

    try:
        response = requests.post(url, json=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print("Błąd:", e)

