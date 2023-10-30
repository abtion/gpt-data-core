# gpt-data-core
When we start a new GPT project and we need to create a new Redis DB and populate it with data - we need to follow these steps:

1. Copy locally an existing gpt-data project. For example gpt-data-kvindekroppen
2. Rename it - so it has the name of the new project you are creating. For example gpt-data-infare
3. Delete the data folder with its content and create an empty data folder in the root of the project
4. Delete the data-temp folder with its content and create an empty data-temp folder in the root of the project
5. Delete the venv folder(if there is one)
6. Go to the folder on your computer and allow the hidden files to be seen. Delete the .git folder. This will remove the link between the old github respository and the project.
7. Go to Abtions github account and click Create New Repository
8. Add name
9. Leave all the rest as it is and click Create repository
10. Go to Redis online, login with Abtions account and create a new DB
11. Go back to VSCode where you have the new gpt-data project created and update the .env file with the new Redis credentials
12. Follow the steps below, to create embeddings and ingest them in the redis DB

## Environment variables

Ensure your .env variables are up to date with at least:

- REDIS_HOST
- REDIS_PORT
- REDIS_PASSWORD
- OPENAI_API_KEY

## Use a python virtual environment (venv)

Create a venv folder, if there is no venv folder in the root directory of the project. If you have the venv folder, you do not need to create one. OBS: If you get an error in one of the following steps, delete the venv folder and create a new one with the command below:

```bash
python -m venv venv
```

Activate venv whenever working on this project. OBS: two different commands below, depending on your operating system:

Windows:

```bash
. venv/scripts/activate
```

Mac:

```bash
. venv/bin/activate
```

Your terminal will display the name of your venv when active: _(venv)_.

Installing the required packages:

```bash
pip install -r requirements.txt
```

If any packages are installed/updated while developing, remember to freeze the package list:

```bash
pip freeze > requirements.txt
```

If you move to another project, close the terminal to deactive the current venv.

## Installing / updating the core package

```bash
pip install git+https://github.com/abtion/gpt-data-core.git
```

## Example use of gpt-data-core

```python
# create_embeddings.py
from gpt_data_core import embedding_generator, config

openAIConfig = config.Config()

generator = embedding_generator.EmbeddingGenerator(
    openAIConfig.OPENAI_API_KEY,
    openAIConfig.DEFAULT_DATA_PATH,
    openAIConfig.DEFAULT_TEMP_PATH
)

generator.process_file("path/to/file")
# generator.process_all_files()

```

```python
# ingest_embeddings.py
from gpt_data_core import embedding_ingestor, config, base_schema, redis_client

openAIConfig = config.Config()

def process_file(pipe, embedding_path, data_path, ingestor: embedding_ingestor.EmbeddingIngestor):
    embedding = ingestor.read_json_embedding(embedding_path)
    data = None
    with open(data_path, "r", encoding="utf8") as f:
        data = f.read()

    ingestor.insert_embedding(
        pipe,
        os.path.basename(data_path),
        data,
        embedding,
    )

redisClient = redis_client.RedisClient(
    openAIConfig.REDIS_HOST,
    openAIConfig.REDIS_PORT,
    openAIConfig.REDIS_PASSWORD)

ingestor = embedding_ingestor.EmbeddingIngestor(
    redisClient,
    openAIConfig.VECTOR_DIMENSIONS,
    openAIConfig.INDEX_NAME,
    openAIConfig.DOC_PREFIX,
    openAIConfig.DEFAULT_DATA_PATH,
    openAIConfig.DEFAULT_TEMP_PATH
)

schema = base_schema.create_base_schema(openAIConfig.VECTOR_DIMENSIONS)
ingestor.create_index(schema)

pipe = ingestor.redis_client.pipeline()

embeddings_and_data_list = ingestor.collect_embedding_and_data_paths()
for embeddings_and_data in embeddings_and_data_list:
    process_file(
        pipe, embeddings_and_data[0], embeddings_and_data[1], ingestor)

pipe.execute()
```

## Additional Redis DB Fields

Sometimes we want to add additional fields to the Database which our chat application needs.

Ensure you configure the Redis schema with the correct type of field, and populate the value when inserting the embedding:

```python
# ingest_embeddings.py
from gpt_data_core import ..., base_schema
from redis.commands.search.field import TagField

def process_file(...):
    ...
    newFieldValue = "some-value"
    ingestor.insert_embedding(
        ...
        extraMapping={"newfield": newFieldValue}
    )

schema = base_schema.create_base_schema(openAIConfig.VECTOR_DIMENSIONS)
abtionschema = schema + (TagField("newfield"),)

...

```
