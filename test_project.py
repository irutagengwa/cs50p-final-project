import pytest

from project import validate_terms, describe_correlation, get_available_terms


TERMS = ["flu symptoms", "pumpkin spice", "recession", "unemployment benefits"]


def test_validate_terms():
    # a good pair passes
    assert validate_terms("recession", "flu symptoms", TERMS) is None

    # made up or missing terms are rejected
    assert validate_terms("bananas", "recession", TERMS) is not None
    assert validate_terms(None, None, TERMS) is not None

    # the same term twice would always give r = 1.00, so it is rejected too
    assert validate_terms("recession", "recession", TERMS) is not None


def test_describe_correlation():
    assert describe_correlation(0.95) == "Very strong positive relationship"
    assert describe_correlation(-0.7) == "Strong negative relationship"
    assert describe_correlation(0.5) == "Moderate positive relationship"
    assert describe_correlation(-0.3) == "Weak negative relationship"
    assert describe_correlation(0.01) == "Essentially no positive relationship"


def test_get_available_terms():
    terms = get_available_terms()
    assert isinstance(terms, list)
    assert len(terms) > 0
    # the query is DISTINCT and ORDER BY, so no duplicates and already sorted
    assert terms == sorted(set(terms))


if __name__ == "__main__":
    pytest.main([__file__])
