from ess_json_schema.validate import validate_json
from jsonschema.exceptions import ValidationError
from datetime import datetime, UTC
from pytest import raises

URI = 'https://ess.eu/efu/caen/calibration/detector'


def test_efu_caen_calibration_detector_validation():
    data = {
        'date': datetime.now(UTC).isoformat(),
        'groups': 2,
        'info': 'Some information for you',
        'instrument': 'INSTRUMENT',
        'units': 1,
        'version': 0,
        'parameters': [
            {
                'groupindex': 0,
                'intervals': [[0, 0.9]],
                'polynomials': [[0, 0, 0, 0]],
                'thresholds': [[0, 1]]
            },
            {
                'groupindex': 1,
                'intervals': [[0.2, 1]],
                'polynomials': [[0, 0, 0, 0]],
                'thresholds': [[0, 1000]]
            },
        ]
    }
    assert validate_json(data, uri=URI)


def test_efu_caen_calibration_detector_fails_on_repeated_groups():
    data = {
        'date': datetime.now(UTC).isoformat(),
        'groups': 2,
        'info': 'Some information for you',
        'instrument': 'INSTRUMENT',
        'units': 1,
        'version': 0,
        'parameters': [
            {
                'groupindex': 0,
                'intervals': [[0, 0.9]],
                'polynomials': [[0, 0, 0, 0]],
                'thresholds': [[0, 1]]
            },
            {
                'groupindex': 0,
                'intervals': [[0, 0.9]],
                'polynomials': [[0, 0, 0, 0]],
                'thresholds': [[0, 1]]
            }
        ]
    }
    with raises(ValidationError) as ex:
        validate_json(data, uri=URI)
    assert 'non-unique' in str(ex.value)


def test_efu_caen_calibration_detector_fails_without_group_count():
    data = {
        'date': datetime.now(UTC).isoformat(),
        'groups': 0,
        'info': 'Some information for you',
        'instrument': 'INSTRUMENT',
        'units': 1,
        'version': 0,
        'parameters': []
    }
    with raises(ValidationError) as ex:
        validate_json(data, uri=URI)
    assert 'less than the minimum' in str(ex.value)


def test_efu_caen_calibration_detector_fails_without_groups():
    data = {
        'date': datetime.now(UTC).isoformat(),
        'groups': 110,
        'info': 'Some information for you',
        'instrument': 'INSTRUMENT',
        'units': 1,
        'version': 0,
        'parameters': []
    }
    with raises(ValidationError) as ex:
        validate_json(data, uri=URI)
    assert 'should be non-empty' in str(ex.value)