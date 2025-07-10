import pytest

from pypi.helpers import filename_is_allowed, normalize


@pytest.mark.parametrize(
    "filename, expected_result",
    [
        ("something.whl", True),
        ("something.WHL", True),
        ("something.tar.gz", True),
        ("something.tar.bz2", True),
        ("something.zip", True),
        ("some_other_thing", False),
        ("something.pdf", False),
    ],
)
def test_filename_is_allowed(filename, expected_result):
    assert filename_is_allowed(filename) is expected_result


@pytest.mark.parametrize(
    "package_name, expected_result",
    [
        ("has_underscores", "has-underscores"),
        ("has-dash_And_uppercase", "has-dash-and-uppercase"),
        ("has_period.and-other-delimiters", "has-period-and-other-delimiters"),
    ],
)
def test_normalize_package_name(package_name, expected_result):
    assert normalize(package_name) == expected_result
