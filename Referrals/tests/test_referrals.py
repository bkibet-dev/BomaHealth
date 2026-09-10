import pytest

from db import init_db
from referrals import ReferralService


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "test_bomahealth.db"
    init_db(path)
    return path


def test_creates_referral_with_valid_data(db_path):
    service = ReferralService(db_path)
    result = service.create_referral(
        referral_id="R001", chp_id="CHP01", household_id="H001", reason="Malnutrition signs"
    )
    assert result.referral_id == "R001"
    assert result.chp_id == "CHP01"
    assert result.household_id == "H001"
    assert result.status == "open"


def test_referral_defaults_to_open_status(db_path):
    service = ReferralService(db_path)
    result = service.create_referral(referral_id="R002", chp_id="CHP01", household_id="H002")
    assert result.status == "open"


def test_raises_error_for_missing_chp_id(db_path):
    service = ReferralService(db_path)
    with pytest.raises(ValueError):
        service.create_referral(referral_id="R003", chp_id=None, household_id="H003")


def test_raises_error_for_missing_household_id(db_path):
    service = ReferralService(db_path)
    with pytest.raises(ValueError):
        service.create_referral(referral_id="R004", chp_id="CHP01", household_id=None)


def test_raises_error_for_duplicate_referral_id(db_path):
    service = ReferralService(db_path)
    service.create_referral(referral_id="R005", chp_id="CHP01", household_id="H005")
    with pytest.raises(ValueError):
        service.create_referral(referral_id="R005", chp_id="CHP02", household_id="H006")


def test_get_referral_returns_existing_referral(db_path):
    service = ReferralService(db_path)
    service.create_referral(referral_id="R006", chp_id="CHP01", household_id="H006")

    result = service.get_referral("R006")
    assert result is not None
    assert result.referral_id == "R006"
    assert result.chp_id == "CHP01"


def test_get_referral_returns_none_for_unknown_id(db_path):
    service = ReferralService(db_path)
    result = service.get_referral("does-not-exist")
    assert result is None


def test_list_referrals_for_chp_returns_only_that_chps_referrals(db_path):
    service = ReferralService(db_path)
    service.create_referral(referral_id="R007", chp_id="CHP01", household_id="H007")
    service.create_referral(referral_id="R008", chp_id="CHP01", household_id="H008")
    service.create_referral(referral_id="R009", chp_id="CHP02", household_id="H009")

    results = service.list_referrals_for_chp("CHP01")
    ids = {r.referral_id for r in results}

    assert ids == {"R007", "R008"}


def test_list_referrals_for_chp_returns_empty_list_for_chp_with_none(db_path):
    service = ReferralService(db_path)
    results = service.list_referrals_for_chp("CHP-with-no-referrals")
    assert results == []