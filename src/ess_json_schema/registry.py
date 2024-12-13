from pathlib import Path


SCHEMA_PREFIX="https://ess.eu/"

# Small schema can be worth loading into memory, e.g., at module import time
# but such an action impacts load-time and memory use so probably should not be
# used for all possible schema
PRELOAD_SCHEMA = {
    f'{SCHEMA_PREFIX}efu/caen/calibration/detector',
    f'{SCHEMA_PREFIX}efu/caen/calibration/group',
}


def find_schema_file(name: str):
    """Find a schema file in the ess_json_schema package"""
    from importlib.resources import files
    from importlib.metadata import distribution
    from json import loads
    if isinstance(name, Path):
        name = name.as_posix()
    if files('ess_json_schema').joinpath(name).is_file():
        return files('ess_json_schema').joinpath(name)
    info = loads(distribution('ess_json_schema').read_text('direct_url.json'))
    if 'dir_info' in info and 'editable' in info['dir_info'] and info['dir_info']['editable'] and 'url' in info:
        path = Path(info['url'].split('file://')[1]).joinpath('ess_json_schema', name)
        return path if path.is_file() else None
    return None


def retrieve_schema(uri: str):
    from referencing import Resource
    from referencing.exceptions import NoSuchResource
    from json import loads
    if not uri.startswith(SCHEMA_PREFIX):
        raise NoSuchResource(uri)
    path = find_schema_file(uri.removeprefix(SCHEMA_PREFIX)+".json")
    if not path:
        raise NoSuchResource(path)
    contents = loads(path.read_text())
    return Resource.from_contents(contents)


def make_registry():
    from json import loads
    from loguru import logger
    from referencing import Registry, Resource
    resources = []
    for uri in PRELOAD_SCHEMA:
        if path := find_schema_file(uri.removeprefix(SCHEMA_PREFIX) + ".json"):
            resources.append(
                (uri, Resource.from_contents(loads(path.read_text())))
            )
        else:
            logger.warning(f'Could not find expected JSON Schema file {uri}')

    registry = Registry(retrieve=retrieve_schema).with_resources(resources)
    return registry



