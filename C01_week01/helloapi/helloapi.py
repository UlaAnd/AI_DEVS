
import requests

import prod


def get_auth(task_name="helloapi", key=prod.api_key_devs):
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
        return [data.get("cookie"), token]
    except requests.exceptions.RequestException as e:
        print("Błąd:", e)


def post_answer():
    task = get_task()
    cookie = task[0]
    url = f"https://zadania.aidevs.pl/answer/{task[1]}"
    params = {"answer": f"{cookie}"}

    try:
        response = requests.post(url, json=params)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print("Błąd:", e)

