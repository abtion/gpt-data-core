import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
        self.REDIS_PORT = os.getenv("REDIS_PORT") or 6379
        self.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or None
        self.DEFAULT_DATA_PATH = os.getenv("DEFAULT_DATA_PATH") or "data"
        self.DEFAULT_TEMP_PATH = os.getenv("DEFAULT_TEMP_PATH") or "data-temp"
        self.VECTOR_DIMENSIONS = os.getenv("VECTOR_DIMENSIONS") or 1536
        self.DOC_PREFIX = os.getenv("DOC_PREFIX") or "doc:"
        self.INDEX_NAME = os.getenv("INDEX_NAME") or "index"
