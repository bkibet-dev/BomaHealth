import pytest
from models.referral import Referral
from models.notification import Notification


@pytest.fixture(autouse=True)
def reset_state():
    Referral.all_referrals = []
    Notification.all_notifications = []
    yield
    Referral.all_referrals = []
    Notification.all_notifications = []


def test_notify_succeeds_for_existing_referral():
    Referral.create_referral(referral_id="R001", chp_id="CHP01", household_id="H001")
    n = Notification.notify(referral_id="R001", chp_id="CHP01")
    assert n.status == "sent"


def test_raises_error_for_nonexistent_referral():
    with pytest.raises(ValueError):
        Notification.notify(referral_id="does-not-exist", chp_id="CHP01")


def test_raises_error_for_duplicate_notification():
    Referral.create_referral(referral_id="R002", chp_id="CHP01", household_id="H002")
    Notification.notify(referral_id="R002", chp_id="CHP01")
    with pytest.raises(ValueError):
        Notification.notify(referral_id="R002", chp_id="CHP01")


def test_save_and_load_round_trip(tmp_path):
    filepath = tmp_path / "notifications.json"
    Referral.create_referral(referral_id="R003", chp_id="CHP01", household_id="H003")
    Notification.notify(referral_id="R003", chp_id="CHP01")
    Notification.save_to_file(filepath)

    Notification.all_notifications = []
    Notification.load_from_file(filepath)

    assert len(Notification.all_notifications) == 1
    assert Notification.all_notifications[0].referral_id == "R003"