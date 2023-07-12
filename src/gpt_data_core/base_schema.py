from redis.commands.search.field import TagField, TextField, VectorField


def create_base_schema(vector_dimensions: int):
    schema = (
        TagField("tag"),
        TextField("content"),
        VectorField(
            "vector",
            "FLAT",  # FLAT OR HSNW
            {
                "TYPE": "FLOAT32",  # FLOAT32 or FLOAT64
                        # Number of Vector Dimensions
                        "DIM": int(vector_dimensions),
                        "DISTANCE_METRIC": "COSINE",  # Vector Search Distance Metric
            },
        ),
        TextField("filename"),
    )
    return schema
