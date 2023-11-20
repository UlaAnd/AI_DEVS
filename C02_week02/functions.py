
from controller_api import ControllerApi


class Task:
    
    def function(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="functions")
        data = controller_api.get_task(token=token)
        task_answer = self.get_answer()
        controller_api.post_answer(task_answer=task_answer, token=token)

    def get_answer(self):
        function = {
            "name": "addUser",
            "description": "przyjmuje jako parametr obiekt",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "surname": {
                        "type": "string",
                    },
                    "year": {
                        "type": "integer",
                    }
                }
            }
        }
        return function


if __name__ == '__main__':
    task = Task()
    task.function()


