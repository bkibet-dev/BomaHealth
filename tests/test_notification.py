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


def test_get_all_notifications_returns_everything():
    Referral.create_referral(referral_id="R030", chp_id="CHP01", household_id="H030")
    Referral.create_referral(referral_id="R031", chp_id="CHP02", household_id="H031")
    Notification.notify(referral_id="R030", chp_id="CHP01")
    Notification.notify(referral_id="R031", chp_id="CHP02")

    all_notifications = Notification.get_all_notifications()
    ids = {n.referral_id for n in all_notifications}
    assert ids == {"R030", "R031"}


def test_raises_error_for_missing_chp_id():
    Referral.create_referral(referral_id="R032", chp_id="CHP01", household_id="H032")
    with pytest.raises(ValueError):
        Notification.notify(referral_id="R032", chp_id=None)


def test_raises_error_for_missing_referral_id():
    with pytest.raises(ValueError):
        Notification.notify(referral_id=None, chp_id="CHP01")


def test_load_from_file_handles_corrupt_json(tmp_path):
    filepath = tmp_path / "corrupt.json"
    filepath.write_text("{not valid json")

    Referral.create_referral(referral_id="R033", chp_id="CHP01", household_id="H033")
    Notification.notify(referral_id="R033", chp_id="CHP01")
    Notification.load_from_file(filepath)

    assert Notification.get_notification_for_referral("R033") is not None