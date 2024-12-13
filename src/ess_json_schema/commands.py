import typer
from pathlib import Path


def get_file_json(filename: Path):
    from json import load
    with filename.open('r') as file:
        data = load(file)
    return data


def validate_json(filename: Path):
    from loguru import logger
    from .validate import validate_json
    data = get_file_json(filename)
    if '$schema' not in data:
        logger.error(f'data does not contain a top-level "$schema" entry')
        return
    validate_json(data['data'], uri=data['$schema'])
    logger.info(f"Validation successful: {filename} against {data['$schema']}")


def validate_schema(filename: Path):
    from loguru import logger
    from jsonschema import Draft202012Validator
    schema = get_file_json(filename)
    schema['$schema'] = Draft202012Validator.META_SCHEMA['$id']
    Draft202012Validator.check_schema(schema)
    logger.info(f"Validation successful: {filename} against {schema}")


def validate(filename: Path, schema: bool=False):
    if schema:
        validate_schema(filename)
    else:
        validate_json(filename)


def validate_cli():
    typer.run(validate)

if __name__ == '__main__':
    typer.run(validate)