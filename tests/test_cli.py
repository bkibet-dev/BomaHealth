import pytest

from Referrals import ReferralService
from Notifications import NotificationService
from cli import create_referral_flow, list_referrals_flow, notify_flow


@pytest.fixture
def referrals_json(tmp_path):
    return tmp_path / "referrals.json"


@pytest.fixture
def notifications_json(tmp_path):
    return tmp_path / "notifications.json"


def _fake_input(*answers):
    """Returns a function that yields each answer in order, like a
    user typing responses to sequential input() prompts."""
    answers_iter = iter(answers)
    return lambda prompt="": next(answers_iter)


def test_create_referral_flow_success(monkeypatch, capsys, referrals_json):
    monkeypatch.setattr("builtins.input", _fake_input("R001", "CHP01", "H001", "Fever"))
    service = ReferralService(referrals_json)

    create_referral_flow(service)

    captured = capsys.readouterr()
    assert "created" in captured.out.lower()
    assert service.get_referral("R001") is not None


def test_create_referral_flow_shows_friendly_error_on_missing_chp(monkeypatch, capsys, referrals_json):
    monkeypatch.setattr("builtins.input", _fake_input("R002", "", "H002", ""))
    service = ReferralService(referrals_json)

    create_referral_flow(service) 

    captured = capsys.readouterr()
    assert "⚠️" in captured.out
    assert service.get_referral("R002") is None


def test_list_referrals_flow_shows_referrals(monkeypatch, capsys, referrals_json):
    service = ReferralService(referrals_json)
    service.create_referral(referral_id="R010", chp_id="CHP01", household_id="H010")
    service.create_referral(referral_id="R011", chp_id="CHP01", household_id="H011")

    monkeypatch.setattr("builtins.input", _fake_input("CHP01"))
    list_referrals_flow(service)

    captured = capsys.readouterr()
    assert "R010" in captured.out
    assert "R011" in captured.out


def test_list_referrals_flow_shows_message_when_none_found(monkeypatch, capsys, referrals_json):
    service = ReferralService(referrals_json)
    monkeypatch.setattr("builtins.input", _fake_input("CHP-with-nothing"))

    list_referrals_flow(service)

    captured = capsys.readouterr()
    assert "no referrals found" in captured.out.lower()


def test_notify_flow_success(monkeypatch, capsys, referrals_json, notifications_json):
    ReferralService(referrals_json).create_referral(
        referral_id="R020", chp_id="CHP01", household_id="H020"
    )
    notif_service = NotificationService(notifications_json, referrals_json)

    monkeypatch.setattr("builtins.input", _fake_input("R020", "CHP01"))
    notify_flow(notif_service)

    captured = capsys.readouterr()
    assert "sent" in captured.out.lower()


def test_notify_flow_shows_friendly_error_for_nonexistent_referral(
    monkeypatch, capsys, referrals_json, notifications_json
):
    notif_service = NotificationService(notifications_json, referrals_json)

    monkeypatch.setattr("builtins.input", _fake_input("does-not-exist", "CHP01"))
    notify_flow(notif_service)  # should not raise — decorator catches it

    captured = capsys.readouterr()
    assert "⚠️" in captured.out

def test_run_menu_full_flow_create_list_notify_then_exit(
    monkeypatch, capsys, referrals_json, notifications_json
):
    from cli import run_menu
    inputs = iter([
        "1", "R001", "CHP01", "H001", "Fever",
        "2", "CHP01",
        "3", "R001", "CHP01",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    run_menu(referrals_json, notifications_json)

    captured = capsys.readouterr()
    assert "created" in captured.out.lower()
    assert "R001" in captured.out
    assert "sent" in captured.out.lower()
    assert "goodbye" in captured.out.lower()


def test_run_menu_handles_invalid_option_then_exits(
    monkeypatch, capsys, referrals_json, notifications_json
):
    from cli import run_menu

    inputs = iter(["9", "0"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    run_menu(referrals_json, notifications_json)

    captured = capsys.readouterr()
    assert "invalid option" in captured.out.lower()
    assert "goodbye" in captured.out.lower()