def version():
    import importlib.metadata as importlib_metadata
    try:
        return importlib_metadata.version("ess_json_schema")
    except importlib_metadata.PackageNotFoundError:
        return "dev"

