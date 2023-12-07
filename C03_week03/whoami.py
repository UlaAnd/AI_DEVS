from controllers.controller_ai import OpenAiController
from controllers.controller_api import ControllerApi


class Task:

    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="whoami")
        data = controller_api.get_task(token=token)
        hint = data.get("hint")
        task_answer = self.get_answer(hint=hint)
        controller_api.post_answer(task_answer=task_answer, token=token)

    def get_hint(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="whoami")
        data = controller_api.get_task(token=token)
        hint = data.get("hint")
        return hint

    def get_answer(self, hint):
        prompt = f'{hint}'
        system = f'I am guessing who about this info is. If I dont know in 100% I answer "0", If I know I send only full name'
        controller = OpenAiController()
        result = controller.get_completion(prompt=prompt, system=system)
        if "0" in result:
            hint2 = self.get_hint()
            another_hint = f'{hint},{hint2}'
            result = self.get_answer(another_hint)

        return result


if __name__ == '__main__':
    task = Task()
    task.main_method()
