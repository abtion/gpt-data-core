import json
import os
import openai


class EmbeddingGenerator():

    def __init__(self, api_key: str, data_path: str, embedding_path: str, embedding_model: str = "text-embedding-ada-002"):
        self.api_key = api_key
        self.data_path = data_path
        self.embedding_path = embedding_path
        self.embedding_model = embedding_model

    def call_openai_embedding_api(self, text):
        openai.api_key = self.api_key
        response = openai.Embedding.create(
            model=self.embedding_model,
            input=text,
        )
        return response

    def process_file(self, file_path):
        file_content = ""
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                file_content += line.strip()

        response = self.call_openai_embedding_api(file_content)

        output_file = self.embedding_path + \
            file_path.removeprefix(self.data_path)

        output_dir = os.path.dirname(output_file)
        if (not os.path.exists(output_dir)):
            os.makedirs(output_dir)

        json_file_path = os.path.splitext(output_file)[0] + ".json"
        with open(json_file_path, "w") as f:
            json.dump(response, f)

        print(
            f"Saved query embedding for {os.path.basename(file_path)} in {json_file_path}"
        )

    def process_all_files(self):
        errors = []
        for root, _, files in os.walk(self.data_path):
            for file in files:
                if (os.path.splitext(file_path)[1] != ".json"):
                    file_path = os.path.join(root, file)
                    try:
                        self.process_file(file_path)
                    except Exception as error:
                        errors.append((file_path, error))
        if len(errors) > 0:
            print("\nERROR while processing files:")
            for error in errors:
                print(f"{error[0]}: '{error[1]}'\n")
