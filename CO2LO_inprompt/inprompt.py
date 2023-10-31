
from ai_controller import OpenAiController
from controller_api import ControllerApi


class Task:
    def inprompt(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="inprompt")
        data = controller_api.get_task(token=token)
        msg = data.get("msg")
        question = data.get("question")
        info_list = data.get("input")
        task_answer = self.get_answer(question=question, info_list=info_list)
        controller_api.post_answer(task_answer=task_answer, token=token)


    def get_answer(self, question: str, info_list: list):
        words = question.split()
        for word in words:
            if word.istitle():
                name = word.rstrip('.?!')
        researched_list = []
        for info in info_list:
            if name in info:
                researched_list.append(info)
        controller = OpenAiController()
        system = f"Odpowiadasz tylko na podstawie informacji z poniższej listy: {researched_list}"
        prompt = f"Odpowiedz po polsku na pytanie: {question}"
        result = controller.get_completion(prompt=prompt, system=system)
        return result


if __name__ == '__main__':
    task = Task()
    task.inprompt()
