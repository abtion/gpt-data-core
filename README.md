# gpt-data-core

## Environment variables

Ensure your .env variables are up to date with at least:

- REDIS_HOST
- REDIS_PORT
- REDIS_PASSWORD
- OPENAI_API_KEY

## Use a python virtual environment (venv)

If no venv exists:

```bash
python -m venv venv
```

Activate venv whenever working on this project:

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
