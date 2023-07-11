import openai


class EmbeddingGenerator():

    def __init__(self, api_key: str, embedding_model: str = "text-embedding-ada-002"):
        self.api_key = api_key
        self.embedding_model = embedding_model

    def call_openai_embedding_api(self, text):
        openai.api_key = self.api_key
        response = openai.Embedding.create(
            model=self.embedding_model,
            input=text,
        )
        return response
