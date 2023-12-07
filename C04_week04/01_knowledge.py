import requests

from controllers.controller_ai import OpenAiController
from controllers.controller_api import ControllerApi
import json



class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="knowledge")
        data = controller_api.get_task(token=token)
        question = data.get("question")
        task_answer = self.get_answer(question=question)
        controller_api.post_answer(task_answer=task_answer, token=token)

    def trial_method(self):
        question = "Jaki jest kurs waluty w Niemczech?"
        task_answer = self.get_answer(question=question)


    def get_answer(self, question):
        system = ("Wybierz kategorię pytania, podaj nazwę kraju w j.angielskim, oraz symbol waluty."
                  "Prześlij odpowiedź w formcie JSON : {populacja: 0, kurs walut: 1, wiedza ogólna: 2}"
                  "przykład:"
                  "user: 'podaj populację Francji?'"
                  "asystent : {kategoria: 0, kraj: 'france', waluta: 'EUR' }"
                  )
        controller = OpenAiController()
        category = controller.get_completion(prompt=question, system=system)
        json_category = json.loads(category.replace("'", "\""))
        print(json_category)
        country = json_category.get("kraj")
        currency = json_category.get("waluta")
        print(country)
        index = json_category.get("kategoria")
        if index == 0:
            answer = get_population(country)
        elif index == 1:
            answer = get_currency(currency)
        else:
            answer = get_info(country)
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







#
# if __name__ == '__main__':
#     task = Task()
#     task.main_method()
#     # get_population("greece")


if __name__ == '__main__':
    task = Task()
    task.trial_method()
