import json
import requests


def get_webhook():
    url = f"https://hook.eu2.make.com/urgvxpmryejmapa8ve9nrt63xwtocwac"
    headers = {"Content-Type": "application/json"}

    data = {
                "type": "resource",
                "content": "exampleContent"
            },

    try:
        response = requests.post(url, headers=headers, json=data )
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        print("Błąd:", e)


if __name__ == '__main__':
    get_webhook()
