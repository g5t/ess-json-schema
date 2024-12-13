
def validate_json(data, schema=None, uri=None):
    from jsonschema import Draft202012Validator
    from .registry import make_registry
    registry = make_registry()
    resolver = registry.resolver()
    if schema is None:
        schema = resolver.lookup(uri).contents
    validator = Draft202012Validator(schema, registry=registry)
    validator.validate(data)
    return True
