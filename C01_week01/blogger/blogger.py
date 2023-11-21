
import requests

import prod
from controllers.ai_controller import OpenAiController




def get_auth(task_name="blogger", key=prod.api_key_devs):
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
        return [data.get("blog"), token]
    except requests.exceptions.RequestException as e:
        print("Błąd:", e)


def post_answer():
    task = get_task()
    titles = task[0]
    url = f"https://zadania.aidevs.pl/answer/{task[1]}"
    answer = []
    for title in titles:
        prompt = f"Jakos specjalista w temacie przyrządzania pizzy Margherity, napisz po polsku rozdział do posta na blogu dla tytułu:{title}"
        controller = OpenAiController()
        result = controller.get_completion(prompt=prompt)
        answer.append(result)
    params = {"answer": answer}

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


