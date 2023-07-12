import json
import os
import numpy as np

from gpt_data_core import redis_client
from redis.commands.search.indexDefinition import IndexDefinition, IndexType


class EmbeddingIngestor():

    def __init__(self,
                 redis_client: redis_client.RedisClient,
                 vector_dimensions: int,
                 index_name: str,
                 doc_prefix: str):
        self.redis_client = redis_client
        self.vector_dimensions = vector_dimensions
        self.index_name = index_name
        self.doc_prefix = doc_prefix

    def delete_index(self):
        try:
            self.redis_client.ft(self.index_name).dropindex(
                delete_documents=True)
            print("Index deleted!")
        except:
            print("Index does not exist!")

    def create_index(self, schema):
        try:
            self.redis_client.ft(self.index_name).info()
            print("Index already exists!")
        except:
            definition = IndexDefinition(
                prefix=[self.doc_prefix], index_type=IndexType.HASH)

            self.redis_client.ft(self.index_name).create_index(
                fields=schema, definition=definition)

    def insert_embedding(self,
                         file_path: str,
                         content: str,
                         embedding,
                         extraMapping: dict = None):

        pipe = self.redis_client.pipeline()

        baseMapping = {
            "content": content,
            "vector": np.array(embedding).astype(np.float32).tobytes(),
            "tag": "openai",
            "filename": os.path.basename(file_path)
        }
        if extraMapping is not None:
            baseMapping = {**baseMapping,  **extraMapping}

        pipe.hset(
            f"{self.doc_prefix}{os.path.splitext(file_path)[0]}",
            mapping=baseMapping,
        )

        print(f"Inserted {file_path}")

    def read_json_embedding(self, file_name: str):
        with open(file_name, "r") as f:
            json_data = json.load(f)

        return json_data["data"][0]["embedding"]
