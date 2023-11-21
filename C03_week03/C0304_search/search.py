import requests

from controllers.ai_controller import OpenAiController
from controllers.controller_api import ControllerApi
from prod import ula_key
import json
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, Distance, VectorParams, PointStruct
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv


def get_data():
    url = "https://unknow.news/archiwum.json"
    response = requests.get(url)
    if response.status_code >= 200:
        data = response.json()
        content = response.content
        selected_data = data[:300]
        with open("./archiwum_selected2.json", "w") as json_file:
            json.dump(content, json_file)
    return selected_data


class Task:
    def main_method(self):
        controller_api = ControllerApi()
        token = controller_api.get_auth(task_name="search")
        data = controller_api.get_task(token=token)
        question = data.get("question")
        task_answer = self.create_collection(question=question)
        controller_api.post_answer(task_answer=task_answer, token=token)

    def get_answer(self, url, question):

        controller = OpenAiController()
        result = controller.get_completion(prompt=question, system=system)
        return result

    def create_collection(self, question):
        load_dotenv(find_dotenv())
        MEMORY_PATH = "archiwum_selected.json"
        COLLECTION_NAME = "archiwum"

        qdrant = QdrantClient("localhost", port=6333)
        embeddings = OpenAIEmbeddings(openai_api_key=ula_key)
        query = question
        query_embedding = embeddings.embed_query(query)
        result = qdrant.get_collections()

        indexed = None
        for collection in result.collections:
            if collection.name == COLLECTION_NAME:
                indexed = collection
                break

        # Create collection if not exists
        if not indexed:
            qdrant.create_collection(
                COLLECTION_NAME,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                on_disk_payload=True
            )

        collection_info = qdrant.get_collection(COLLECTION_NAME)

        # Add data to collection if empty
        if not collection_info.points_count:
            # Read File
            with open(MEMORY_PATH, 'r') as f:
                memory = json.load(f)

            documents_with_meta = []
            for document in memory:
                title = document['title']
                content = document['info']
                url = document['url']
                document_with_meta = [
                    {
                        'source': COLLECTION_NAME,
                        'title': title,
                        'content': content,
                        'url': url,
                        'uuid': str(uuid.uuid4())
                    }
                ]
                documents_with_meta.append(document_with_meta)
            # Generate embeddings and index
            points = []
            for document in documents_with_meta[:300]:
                # print(document)
                embedding = embeddings.embed_query(document[0]['content'])
                points.append({
                    'id': document[0]['uuid'],
                    'payload': document[0],
                    'vector': embedding
                })

            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                wait=True,
                points=[
                    PointStruct(id=point['id'], vector=point['vector'], payload=point['payload']) for point in points
                ]
            )


        search_result = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            query_filter=Filter(
                must=[FieldCondition(key="source", match=MatchValue(value=COLLECTION_NAME))]
            ),
            limit=1,
        )
        return search_result[0].payload.get("url")



if __name__ == '__main__':
    task = Task()
    # get_data()
    task.main_method()