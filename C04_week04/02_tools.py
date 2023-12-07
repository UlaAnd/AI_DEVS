from datetime import datetime

import requests

from controllers.controller_ai import OpenAiController
from controllers.controller_api import ControllerApi
import json



class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="tools")
        data = controller_api.get_task(token=token)
        question = data.get("question")
        # question = "Pojutrze mam kupić 1kg ziemniaków"
        task_answer = self.get_answer(question=question)
        controller_api.post_answer(task_answer=task_answer, token=token)


    def get_answer(self, question):
        today_date = datetime.today()
        formatted_date = today_date.strftime('%Y-%m-%d')

        system = ("Decide whether the task should be added to the 'ToDo' list or "
                  "'Calendar' list -(if time is provided or some time/data was mentioned) "
                  f"today date: {formatted_date}"
                  f"Send JSON format"
                  "example : "
                  "user : 'Pojutrze mam kupić 1kg ziemniaków'"
                  "asystent : {'tool': 'Calendar','desc':'kupić 1kg ziemniaków','date':'2023-11-25'}"
                  "user : 'Przypomnij mi, że mam kupić mleko'"
                  "asystent :{'tool': 'ToDo','desc': 'Kup mleko'}"
                  )
        controller = OpenAiController()
        answerr = controller.get_completion(prompt=question, system=system)
        answer = json.loads(answerr.replace("'", "\""))
        print(answer)

        return answer


def get_population(country):
    url = f"https://restcountries.com/v3.1/name/{country}/"
    response = requests.get(url)
    if response.status_code >= 200:
        data = response.json()
        answer = data[0].get("population")
        return answer

def get_currency(currency):
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency}"
    response = requests.get(url)
    if response.status_code >= 200:
        data = response.json()
        answer = data.get("rates").get("mid")
        return answer


if __name__ == '__main__':
    task = Task()
    task.main_method()
    # get_population("greece")


