# gpt-data-core

## Installation and updating to newest package version

Rerun this command to check for and install updates .

```bash
pip install git+https://github.com/abtion/gpt-data-core.git
```

## Usage

Features:

- functions.delete_index --> remove the current Redis DB Index
- functions.create_index --> create a new Redis DB Index
- functions.create_embeddings --> create openai embedding files
- functions.insert_embedding --> insert an embedding file in Redis DB

### Example:

```python
from gpt_data_core import functions

# TODO: add a minimal working example of the basic flow
functions.delete_index(...)
```

## Contributing

Feel free to add relevant core functionality to this package & remember to increment the version in [pyproject.toml](pyproject.toml)
