import os
import pytest

from models.referral import Referral
from models.notification import Notification
from cli.referrals import create_referral_flow
from cli.notifications import notify_flow


@pytest.fixture(autouse=True)
def isolated_data_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("data", exist_ok=True)
    Referral.all_referrals = []
    Notification.all_notifications = []
    yield
    Referral.all_referrals = []
    Notification.all_notifications = []


def test_notify_flow_success(capsys):
    create_referral_flow("R020", "CHP01", "H020")
    capsys.readouterr() 

    notify_flow("R020", "CHP01")

    captured = capsys.readouterr()
    assert "sent" in captured.out.lower()
    assert "R020" in captured.out


def test_notify_flow_raises_for_nonexistent_referral():
    with pytest.raises(ValueError):
        notify_flow("does-not-exist", "CHP01")


def test_notify_flow_raises_for_duplicate():
    create_referral_flow("R021", "CHP01", "H021")
    notify_flow("R021", "CHP01")

    with pytest.raises(ValueError):
        notify_flow("R021", "CHP01")