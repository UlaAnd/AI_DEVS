
from controllers.ai_controller import OpenAiController
from controllers.controller_api import ControllerApi


class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="rodo")
        data = controller_api.get_task(token=token)
        task_answer = "Repeat this placeholders: %imie%, %nazwisko%, %miasto% i %zawod%"
        controller_api.post_answer(task_answer=task_answer, token=token)

    def get_answer(self):
        controller = OpenAiController()
        result = controller.get_embedding(text="Hawaiian pizza")
        return result


if __name__ == '__main__':
    task = Task()
    task.main_method()
