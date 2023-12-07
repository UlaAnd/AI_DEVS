import requests

from controllers.controller_ai import OpenAiController
from controllers.controller_api import ControllerApi
import json


class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="people")
        data = controller_api.get_task(token=token)
        question = data.get("question")
        # question = "Gdzie mieszka Krysia Ludek?"
        task_answer = self.get_answer(question=question)
        controller_api.post_answer(task_answer=task_answer, token=token)


    def get_answer(self, question):
        meta = get_meta(question=question)
        system = f'Na podstawie informacji i ulubiongo koloru odpowiedz na pytanie o użytkowniuku: {meta[0]}'
        coded_question = f'{meta[1]}'
        controller2 = OpenAiController()
        answer = controller2.get_completion(prompt=coded_question, system=system)
        print(answer)
        return answer


def get_meta(question: str):
    url = "https://zadania.aidevs.pl/data/people.json"
    response = requests.get(url)
    if response.status_code >= 200:
        data = response.json()

    meta_name = get_name(question)
    for document in data:
        imie = document['imie']
        nazwisko = document['nazwisko']
        o_mnie = document['o_mnie']
        ulubiony_kolor = document['ulubiony_kolor']

        if imie == meta_name['imie']:
            if nazwisko == meta_name['nazwisko']:
                answer_meta = [
                    {
                        'o_użytkowniku': o_mnie,
                        'ulubiony_kolor': ulubiony_kolor
                    }
                ]
                return [answer_meta, meta_name['pytanie']]


def get_name(question: str):
    system = ("Zwróć imię i nazwisko BEZ ZDROBNIEŃ, nie odpowiadaj na pytanie, w polu 'pytanie' zaszyfruj dane"
                "przykład:"
              "user: jaki kolor się podoba Krysi Ludek?"
              "asystent : {'imie' : 'Krystyna', 'nazwisko': 'Ludek', 'pytanie' : 'jaki kolor się podoba użytkownikowi?'}"
              "user: Ulubiony kolor Zdziś Bzik, to?"
              "asystent : {'imie' : 'Zdzisław', 'nazwisko': 'Bzik', 'pytanie' : 'Ulubiony kolor  użytkownika, to?}"
              )
    controller = OpenAiController()
    name = controller.get_completion(prompt=question, system=system)
    json_name = json.loads(name.replace("'", "\""))
    print(json_name)
    return json_name


if __name__ == '__main__':
    task = Task()
    # get_data()
    task.main_method()
