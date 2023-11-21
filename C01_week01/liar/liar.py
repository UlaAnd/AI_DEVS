import requests

import prod
from controllers.ai_controller import OpenAiController


def get_auth(task_name="liar", key=prod.api_key_devs):
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


def get_task(question):
    token = get_auth()
    url = f"https://zadania.aidevs.pl/task/{token}"
    params = {'question': question}

    try:
        response = requests.post(url, params)
        response.raise_for_status()
        data = response.json()
        print(data)
        return [data.get("answer"), token]
    except requests.exceptions.RequestException as e:
        print("Błąd:", e)


def post_answer():
    question = "What is capital of Poland?"
    task = get_task(question)
    answer = task[0]
    url = f"https://zadania.aidevs.pl/answer/{task[1]}"
    controller = OpenAiController()
    system = (f"Jesteś asystentem, który analizuje czy user odpowiedział poprawnie na pytanie: {question},"
              f"Jeśli odpowiedź usera się zgadza przesyłasz tylko słowo:YES, gdy odpowiedź jest zła przesyłasz :NO")
    result = controller.get_completion(prompt=answer, system=system)
    task_answer = result
    params = {"answer": task_answer}
    try:
        response = requests.post(url, json=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print("Błąd:", e)


if __name__ == '__main__':
    post_answer()
