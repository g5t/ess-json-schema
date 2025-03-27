# JSON Schema based validator for ESS JSON files
The Event Formation Unit, File Writer, and other ESS tools use JSON to communicate
configuration information; sometimes over a network interface and sometimes via
locally available files.

Some of these JSON objects can be edited by an end user, by hand or via a utility.
In order to facilitate ease of interoperability between different producers and 
consumers of this information, the _schema_ that each consumer expects should be
available to allow any producer to validate their produced JSON.

This validator uses internally-defined schema for the following JSON objects

| JSON Consumer        | URI                                          | Representing                                                |
|----------------------|----------------------------------------------|-------------------------------------------------------------|
| Event Formation Unit | https://ess.eu/efu/caen/calibration/detector | Detector-level calibration information for CAEN instruments |
| Event Formation Unit | https://ess.eu/efu/caen/calibration/group    | Calibration information for a group within a CAEN detector  |

Other schema can be added internally or defined externally and retrieved
at validation time.

## Valid schema-friendly JSON data
The root-level object of any to-be validated JSON should contain two items,
The `$schema` entry is used to pick the correct validator, which is then used
against the contents of the `data` object.
```json
{
  "$schema":  "URI of the contained JSON's schema",
  "data": {
    ...
  }
}
```

## Usage
After installing via, e.g., `python -m pip install git+https://github.com/g5t/ess-json-schema`
an entrypoint script `validate` will be available in your environment.

You can use this from a command line interface in the same environment
```cmd
$ validate /path/to/the_file_to_validate.json
```

### Schema-less JSON validation
If you have a JSON file which should conform to a _known_ JSON schema, but which
does not include the special `$schema` entry, you can specify its `uri` in the
call to the validation entrypoint, e.g.,
```cmd
$ validate /path/to/event-formation-unit/src/modules/bifrost/configs/bifrostnullcalib.json --uri https://ess.eu/efu/caen/calibration/detector
```

Note that this variant *does not* validate the main `data` entry name, but instead
expects that the JSON root contains one key which then contains the equivalent of
the `data` entry.