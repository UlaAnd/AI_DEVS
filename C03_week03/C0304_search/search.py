import requests

from ai_controller import OpenAiController
from controller_api import ControllerApi
from prod import ula_key
from qdrant_helper import create_collection
import json
import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, Distance, VectorParams, PointStruct
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv


class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="scraper")
        data = controller_api.get_task(token=token)
        question = data.get("question")
        task_answer = self.get_answer(url=url, question=question)
        controller_api.post_answer(task_answer=task_answer, token=token)

    def get_answer(self, url, question):

        controller = OpenAiController()
        result = controller.get_completion(prompt=question, system=system)
        return result

    def get_data(self):
        url = "https://unknow.news/archiwum.json"
        response = requests.get(url)
        if response.status_code >= 200:
            data = response.json()
            selected_data = data[:300]
            with open("./archiwum_selected.json", "w") as json_file:
                json.dump(selected_data, json_file)
        return selected_data

    def create_collection(self):
        load_dotenv(find_dotenv())
        MEMORY_PATH = "archiwum_selected.json"
        COLLECTION_NAME = "archiwum"

        qdrant = QdrantClient("localhost", port=6333)
        embeddings = OpenAIEmbeddings(openai_api_key=ula_key)
        query = "Dalle-3"
        query_embedding = embeddings.embed_query(query)
        result = qdrant.get_collections()



if __name__ == '__main__':
    task = Task()
    task.get_data()
    # task.main_method()
    # task.create_collections()