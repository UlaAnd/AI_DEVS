from datetime import datetime
from urllib.parse import urlparse

import requests

from controllers.controller_ai import OpenAiController
from controllers.controller_api import ControllerApi
import json



class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="gnome")
        data = controller_api.get_task(token=token)
        url = data.get("url")
        task_answer = self.get_answer(url=url)
        controller_api.post_answer(task_answer=task_answer, token=token)


    def get_answer(self, url):
        # text = "what is in this image ? "
        text = 'I will give you a URL with drawing of a gnome with a hat on his head. Tell me what is the color of the hat in POLISH. If any errors occur, return "ERROR" as answer. If there will be no hat return "ERROR"'
        controller = OpenAiController()
        answerr = controller.get_describtion(text=text, url=url)
        # answer = json.loads(answerr.replace("'", "\""))
        print(answerr)

        return answerr


if __name__ == '__main__':
    task = Task()
    task.main_method()
    # get_population("greece")


