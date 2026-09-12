import pytest
from models.referral import Referral


@pytest.fixture(autouse=True)
def reset_referrals():
    Referral.all_referrals = []
    yield
    Referral.all_referrals = []


def test_creates_referral_with_valid_data():
    r = Referral.create_referral(referral_id="R001", chp_id="CHP01", household_id="H001", reason="Fever")
    assert r.referral_id == "R001"
    assert r.status == "open"


def test_raises_error_for_missing_chp_id():
    with pytest.raises(ValueError):
        Referral.create_referral(referral_id="R002", chp_id=None, household_id="H002")


def test_raises_error_for_duplicate_referral_id():
    Referral.create_referral(referral_id="R003", chp_id="CHP01", household_id="H003")
    with pytest.raises(ValueError):
        Referral.create_referral(referral_id="R003", chp_id="CHP02", household_id="H004")


def test_get_referrals_for_chp_filters_correctly():
    Referral.create_referral(referral_id="R004", chp_id="CHP01", household_id="H004")
    Referral.create_referral(referral_id="R005", chp_id="CHP02", household_id="H005")
    results = Referral.get_referrals_for_chp("CHP01")
    assert len(results) == 1
    assert results[0].referral_id == "R004"


def test_resolve_changes_status():
    r = Referral.create_referral(referral_id="R006", chp_id="CHP01", household_id="H006")
    r.resolve()
    assert r.status == "resolved"


def test_save_and_load_round_trip(tmp_path):
    filepath = tmp_path / "referrals.json"
    Referral.create_referral(referral_id="R007", chp_id="CHP01", household_id="H007")
    Referral.save_to_file(filepath)

    Referral.all_referrals = []
    Referral.load_from_file(filepath)

    assert len(Referral.all_referrals) == 1
    assert Referral.all_referrals[0].referral_id == "R007"


def test_get_all_referrals_returns_everything():
    Referral.create_referral(referral_id="R020", chp_id="CHP01", household_id="H020")
    Referral.create_referral(referral_id="R021", chp_id="CHP02", household_id="H021")
    all_referrals = Referral.get_all_referrals()
    ids = {r.referral_id for r in all_referrals}
    assert ids == {"R020", "R021"}


def test_cancel_changes_status():
    r = Referral.create_referral(referral_id="R022", chp_id="CHP01", household_id="H022")
    r.cancel()
    assert r.status == "cancelled"


def test_raises_error_for_missing_referral_id():
    with pytest.raises(ValueError):
        Referral.create_referral(referral_id=None, chp_id="CHP01", household_id="H023")


def test_raises_error_for_missing_household_id():
    with pytest.raises(ValueError):
        Referral.create_referral(referral_id="R024", chp_id="CHP01", household_id=None)


def test_load_from_file_handles_corrupt_json(tmp_path):
    filepath = tmp_path / "corrupt.json"
    filepath.write_text("{not valid json")

    Referral.create_referral(referral_id="R025", chp_id="CHP01", household_id="H025")
    Referral.load_from_file(filepath)

    assert Referral.get_referral("R025") is not None