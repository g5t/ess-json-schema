from ess_json_schema.validate import validate_json
from pytest import raises

def test_efu_caen_calibration_group_validation():
    data = {
        'groupindex': 1,
        'intervals': [[0, 0.25], [0.251, 0.5], [0.501, 0.75], [0.751, 1]],
        'polynomials': [[0, 0, 0, 0], [1, 1, 1, 1], [2.1, 2.2, 2., 3.4], [0, 0, -1, 2]],
    }
    assert validate_json(data, uri='https://ess.eu/efu/caen/calibration/group')


def test_efu_caen_calibration_group_throws_on_repeated_intervals():
    from jsonschema.exceptions import ValidationError

    repeated_intervals = {
        'groupindex': 1,
        'intervals': [[0, 1], [0, 1], [0, 1], [0, 1]],
        'polynomials': [[0, 0, 0, 0], [1, 1, 1, 1], [2.1, 2.2, 2., 3.4], [0, 0, -1, 2]],
    }
    with raises(ValidationError) as ex:
        validate_json(repeated_intervals, uri='https://ess.eu/efu/caen/calibration/group')

    assert "non-unique" in str(ex.value)


def test_efu_caen_calibration_group_throws_on_missing_values():
    from jsonschema.exceptions import ValidationError

    repeated_intervals = {
        'groupindex': 1,
        'intervals': [[0, 1]],
        'polynomials': [[0, 0, 0]]
    }
    with raises(ValidationError) as ex:
        validate_json(repeated_intervals,
                      uri='https://ess.eu/efu/caen/calibration/group')

    assert "does not contain items" in str(ex.value)


def test_efu_caen_calibration_group_throws_on_disallowed_values():
    from jsonschema.exceptions import ValidationError

    repeated_intervals = {
        'groupindex': 1,
        'intervals': [[0, 10]],
        'polynomials': [[0, 0, 0]],
    }
    with raises(ValidationError) as ex:
        validate_json(repeated_intervals,
                      uri='https://ess.eu/efu/caen/calibration/group')

    assert "does not contain items" in str(ex.value)


def test_efu_caen_calibration_group_throws_on_disallowed_types():
    from jsonschema.exceptions import ValidationError

    repeated_intervals = {
        'groupindex': 3.14159,
        'intervals': [[0, 1]],
        'polynomials': [[0, 0, 0]],
    }
    with raises(ValidationError) as ex:
        validate_json(repeated_intervals,
                      uri='https://ess.eu/efu/caen/calibration/group')

    assert "is not of type 'integer'" in str(ex.value)