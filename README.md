# gpt-data-core

## Environment variables

Ensure your .env variables are up to date with at least:

- REDIS_HOST
- REDIS_PORT
- REDIS_PASSWORD
- OPENAI_API_KEY
- DEFAULT_DATA_PATH

## Use a python virtual environment (venv)

If no venv exists:

```bash
python -m venv venv
```

Activate venv whenever working on this project:

```bash
. venv/scripts/activate (Windows)
. venv/bin/activate (Mac)
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

generator = embedding_generator.EmbeddingGenerator(api_key = openAIConfig.OPENAI_API_KEY)

response = generator.call_openai_embedding_api("some-text")
```
