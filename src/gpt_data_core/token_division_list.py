import glob
import tiktoken
from pathlib import Path

class TokenDivisionList:
    def __init__(self, model="gpt-3.5-turbo-16k", max_tokens=8191):
        self.model = model
        self.max_tokens = max_tokens

    def __num_tokens(self, text: str) -> int:
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(text))

    def process_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        number_of_tokens_used = self.__num_tokens(text)

        if number_of_tokens_used < self.max_tokens:
            return

        divisions = -(-number_of_tokens_used // self.max_tokens)  # Ceiling division
        print(f"Number divisions: {divisions} for {file_path}")

    def process_files(self, input_path):
        print(f"Division list (tokenlimit: {self.max_tokens}):")
        for file_path in glob.glob(f"{input_path}/**/*.txt", recursive=True):
            self.process_file(Path(file_path))
