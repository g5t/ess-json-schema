import typer
from pathlib import Path


def get_file_json(filename: Path):
    from json import load
    with filename.open('r') as file:
        data = load(file)
    return data


def validate_uri(filename: Path, uri: str):
    from loguru import logger
    from .validate import validate_json as vj
    data = get_file_json(filename)
    if '$schema' in data and 'data' in data:
        uri = data['$schema']
        data = data['data']
    elif uri is not None and len(data) == 1:
        data = data[next(iter(data))]
    else:
        raise ValueError('Either a valid in-JSON $schema field or a specified URI is required.')

    vj(data, uri=uri)
    logger.info(f"Validation successful: {filename} against {uri}")


def validate_schema(filename: Path):
    from loguru import logger
    from jsonschema import Draft202012Validator
    schema = get_file_json(filename)
    schema['$schema'] = Draft202012Validator.META_SCHEMA['$id']
    Draft202012Validator.check_schema(schema)
    logger.info(f"Validation successful: {filename} against {schema}")


def validate(filename: Path, uri: str=None, schema: bool=False):
    if schema:
        validate_schema(filename)
    else:
        validate_uri(filename, uri)

def validate_cli():
    typer.run(validate)


if __name__ == '__main__':
    typer.run(validate)
