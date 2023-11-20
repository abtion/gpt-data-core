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
            return False

        divisions = -(-number_of_tokens_used // self.max_tokens)  # Ceiling division
        print(f"Number divisions: {divisions} for {file_path}")
        return True

    def process_files(self, input_path):
        print(f"Division list:")
        
        totalCount = 0
        processedCount = 0
        
        for file_path in glob.glob(f"{input_path}/**/*.txt", recursive=True):
            processed = self.process_file(Path(file_path))

            totalCount += 1
            if processed:
                processedCount += 1

        print(f"Model used:    {self.model}")
        print(f"Tokenlimit:    {self.max_tokens}")
        print(f"Total files:   {totalCount}")
        print(f"To be divided: {processedCount}")
