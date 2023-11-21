import requests

from controllers.ai_controller import OpenAiController
from controllers.controller_api import ControllerApi


class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="scraper")
        data = controller_api.get_task(token=token)
        url = data.get("input")
        question = data.get("question")
        task_answer = self.get_answer(url=url, question=question)
        controller_api.post_answer(task_answer=task_answer, token=token)

    def get_answer(self, url, question):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                self.get_answer(url=url, question=question)
            data = response.content
            print(data)
        except requests.exceptions.RequestException as e:
            print("Błąd:", e)
        system = (f'Return answer for the question in POLISH language, based on provided article. Maximum length for '
                  f'the answer is 200 characters. Article : {data}')
        controller = OpenAiController()
        result = controller.get_completion(prompt=question, system=system)
        return result


if __name__ == '__main__':
    task = Task()
    task.main_method()
