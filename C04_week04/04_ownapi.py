from datetime import datetime
from urllib.parse import urlparse

import requests

from controllers.controller_ai import OpenAiController
from controllers.controller_api import ControllerApi
import json



class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="ownapipro")
        task_answer = "https://wishgenerator.onrender.com/generate-replay/"
        controller_api.post_answer(task_answer=task_answer, token=token)


if __name__ == '__main__':
    task = Task()
    task.main_method()
    # get_population("greece")


