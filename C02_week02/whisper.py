from controllers.ai_controller import OpenAiController
from controllers.controller_api import ControllerApi


class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="whisper")
        data = controller_api.get_task(token=token)
        task_answer = self.get_answer()
        controller_api.post_answer(task_answer=task_answer, token=token)

    def get_answer(self):
        controller = OpenAiController()
        # response = requests.get(url="https://zadania.aidevs.pl/data/mateusz.mp3")
        # response.raise_for_status()
        audio_file_path = "/C02_week02/mateusz.mp3"
        result = controller.get_whisper(audio_file_path=audio_file_path)
        return result


if __name__ == '__main__':
    task = Task()
    task.main_method()


