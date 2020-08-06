import validate

# Test license numbers
ESMA_NUMBER = "E142304"
AHA_NUMBER = "195506016954"
ARC_NUMBER = "10FMU9"
DCA_NUMBER = "G 50925"
DCA_LASTNAME = "DOEMENY"

# Expected test results
ESMA_EXPECTED_RESULT = """
FULL NAME: Benjamin Thales Lenington
LICENSE STATUS: Active
LICENSE TYPE: EMT
ISSUE DATE: 9/14/2018
EXP DATE: 9/30/2022
"""

AHA_EXPECTED_RESULT = "TODO"
ARC_EXPECTED_RESULT = "TODO"
DCA_EXPECTED_RESULT = "TODO"


def test_validate_esma():
    test_result = validate.validate_esma(ESMA_NUMBER)
    assert ESMA_EXPECTED_RESULT in test_result


def test_validate_aha():
    test_result = validate.validate_aha(AHA_NUMBER)
    assert test_result == AHA_EXPECTED_RESULT


def test_validate_arc():
    test_result = validate.validate_arc(ARC_NUMBER)
    assert test_result == ARC_EXPECTED_RESULT


def test_validate_dca():
    test_result = validate.validate_dca(DCA_NUMBER)
    assert test_result == DCA_EXPECTED_RESULT
