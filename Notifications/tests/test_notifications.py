import pytest
from notifications import NotificationService

def test_creates_notification_for_valid_referral():
    service = NotificationService()
    result = service.notify(referral_id="R001", chp_id="CHP01")
    assert result.status == "sent"
    assert result.chp_id == "CHP01"
    assert result.referral_id == "R001"

def test_notification_contains_referral_details():
    service = NotificationService()
    result = service.notify(referral_id="R002", chp_id="CHP02")
    assert result.referral_id == "R002"

def test_does_not_duplicate_notification_for_same_referral():
    service = NotificationService()
    service.notify(referral_id="R003", chp_id="CHP01")

    with pytest.raises(ValueError):
        service.notify(referral_id="R003", chp_id="CHP01")

def test_raises_error_for_missing_chp():
    service = NotificationService()
    with pytest.raises(ValueError):
        service.notify(referral_id="R004", chp_id=None)

def test_raises_error_for_missing_referral_id():
    service = NotificationService()
    with pytest.raises(ValueError):
        service.notify(referral_id=None, chp_id="CHP01")
