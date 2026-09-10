import pytest

from db import init_db, get_connection
from notifications import NotificationService


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "test_bomahealth.db"
    init_db(path)
    return path


def make_referral(db_path, referral_id, chp_id, household_id="H001"):
    conn = get_connection(db_path)
    conn.execute(
        "INSERT INTO referrals (referral_id, chp_id, household_id) VALUES (?, ?, ?)",
        (referral_id, chp_id, household_id),
    )
    conn.commit()
    conn.close()

def test_creates_notification_for_valid_referral(db_path):
    make_referral(db_path, "R001", "CHP01")
    service = NotificationService(db_path)

    result = service.notify(referral_id="R001", chp_id="CHP01")

    assert result.status == "sent"
    assert result.chp_id == "CHP01"
    assert result.referral_id == "R001"


def test_notification_is_persisted_in_db(db_path):
    make_referral(db_path, "R002", "CHP02")
    NotificationService(db_path).notify(referral_id="R002", chp_id="CHP02")

    conn = get_connection(db_path)
    row = conn.execute(
        "SELECT * FROM notifications WHERE referral_id = ?", ("R002",)
    ).fetchone()
    conn.close()

    assert row is not None
    assert row["chp_id"] == "CHP02"
    assert row["status"] == "sent"


def test_can_notify_multiple_different_referrals(db_path):
    make_referral(db_path, "R010", "CHP01")
    make_referral(db_path, "R011", "CHP01")
    make_referral(db_path, "R012", "CHP02")
    service = NotificationService(db_path)

    assert service.notify(referral_id="R010", chp_id="CHP01").status == "sent"
    assert service.notify(referral_id="R011", chp_id="CHP01").status == "sent"
    assert service.notify(referral_id="R012", chp_id="CHP02").status == "sent"

def test_does_not_duplicate_notification_for_same_referral(db_path):
    make_referral(db_path, "R003", "CHP01")
    service = NotificationService(db_path)
    service.notify(referral_id="R003", chp_id="CHP01")

    with pytest.raises(ValueError):
        service.notify(referral_id="R003", chp_id="CHP01")


def test_duplicate_prevented_even_across_service_instances(db_path):
    make_referral(db_path, "R013", "CHP01")
    NotificationService(db_path).notify(referral_id="R013", chp_id="CHP01")

    with pytest.raises(ValueError):
        NotificationService(db_path).notify(referral_id="R013", chp_id="CHP01")

def test_raises_error_for_missing_chp(db_path):
    make_referral(db_path, "R004", "CHP01")
    service = NotificationService(db_path)
    with pytest.raises(ValueError):
        service.notify(referral_id="R004", chp_id=None)

def test_raises_error_for_missing_referral_id(db_path):
    service = NotificationService(db_path)
    with pytest.raises(ValueError):
        service.notify(referral_id=None, chp_id="CHP01")

def test_raises_error_for_whitespace_only_chp_id(db_path):
    make_referral(db_path, "R006", "CHP01")
    service = NotificationService(db_path)
    with pytest.raises(ValueError):
        service.notify(referral_id="R006", chp_id="   ")

def test_raises_error_for_referral_that_does_not_exist(db_path):
    service = NotificationService(db_path)
    with pytest.raises(ValueError):
        service.notify(referral_id="R999-does-not-exist", chp_id="CHP01")