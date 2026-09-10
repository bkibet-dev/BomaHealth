import pytest
def validate_chp_id(value):
    pass

def validate_household_id(value):
    pass

def validate_referral_status(value):
    pass

def test_validate_chp_id_valid():
    assert validate_chp_id('CHP001') == True
    assert validate_chp_id('123') == False
    assert validate_chp_id(None) == False

def test_validate_household_id_valid():
    assert validate_household_id('HH001') == True
    assert validate_household_id('') == False
    assert validate_household_id(None) == False

def test_validate_referral_status_valid():
    assert validate_referral_status('pending') == True
    assert validate_referral_status('resolved') == True
    assert validate_referral_status('invalid') == False
    assert validate_referral_status(None) == False