import pytest

from notifications import NotificationService
from referrals import ReferralService


@pytest.fixture
def referrals_json(tmp_path):
    return tmp_path / "referrals.json"


@pytest.fixture
def notifications_json(tmp_path):
    return tmp_path / "notifications.json"


def make_referral(referrals_json, referral_id, chp_id, household_id="H001"):
    """Test helper: create a real referral so notify() has something
    valid to reference."""
    ReferralService(referrals_json).create_referral(
        referral_id=referral_id, chp_id=chp_id, household_id=household_id
    )


def test_creates_notification_for_valid_referral(notifications_json, referrals_json):
    make_referral(referrals_json, "R001", "CHP01")
    service = NotificationService(notifications_json, referrals_json)

    result = service.notify(referral_id="R001", chp_id="CHP01")

    assert result.status == "sent"
    assert result.chp_id == "CHP01"
    assert result.referral_id == "R001"


def test_notification_persists_across_service_instances(notifications_json, referrals_json):
    make_referral(referrals_json, "R002", "CHP02")
    NotificationService(notifications_json, referrals_json).notify(
        referral_id="R002", chp_id="CHP02"
    )

    fresh_service = NotificationService(notifications_json, referrals_json)
    with pytest.raises(ValueError):
        fresh_service.notify(referral_id="R002", chp_id="CHP02")


def test_can_notify_multiple_different_referrals(notifications_json, referrals_json):
    make_referral(referrals_json, "R010", "CHP01")
    make_referral(referrals_json, "R011", "CHP01")
    make_referral(referrals_json, "R012", "CHP02")
    service = NotificationService(notifications_json, referrals_json)

    assert service.notify(referral_id="R010", chp_id="CHP01").status == "sent"
    assert service.notify(referral_id="R011", chp_id="CHP01").status == "sent"
    assert service.notify(referral_id="R012", chp_id="CHP02").status == "sent"


def test_does_not_duplicate_notification_for_same_referral(notifications_json, referrals_json):
    make_referral(referrals_json, "R003", "CHP01")
    service = NotificationService(notifications_json, referrals_json)
    service.notify(referral_id="R003", chp_id="CHP01")

    with pytest.raises(ValueError):
        service.notify(referral_id="R003", chp_id="CHP01")


def test_raises_error_for_missing_chp(notifications_json, referrals_json):
    make_referral(referrals_json, "R004", "CHP01")
    service = NotificationService(notifications_json, referrals_json)
    with pytest.raises(ValueError):
        service.notify(referral_id="R004", chp_id=None)


def test_raises_error_for_missing_referral_id(notifications_json, referrals_json):
    service = NotificationService(notifications_json, referrals_json)
    with pytest.raises(ValueError):
        service.notify(referral_id=None, chp_id="CHP01")


def test_raises_error_for_whitespace_only_chp_id(notifications_json, referrals_json):
    make_referral(referrals_json, "R006", "CHP01")
    service = NotificationService(notifications_json, referrals_json)
    with pytest.raises(ValueError):
        service.notify(referral_id="R006", chp_id="   ")


def test_raises_error_for_referral_that_does_not_exist(notifications_json, referrals_json):
    service = NotificationService(notifications_json, referrals_json)
    with pytest.raises(ValueError):
        service.notify(referral_id="R999-does-not-exist", chp_id="CHP01")