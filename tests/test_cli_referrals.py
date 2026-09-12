import os
import pytest

from models.referral import Referral
from cli.referrals import create_referral_flow, list_referrals_flow


@pytest.fixture(autouse=True)
def isolated_data_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    os.makedirs("data", exist_ok=True)
    Referral.all_referrals = []
    yield
    Referral.all_referrals = []


def test_create_referral_flow_success(capsys):
    create_referral_flow("R001", "CHP01", "H001", "Fever")

    captured = capsys.readouterr()
    assert "created" in captured.out.lower()
    assert "R001" in captured.out
    assert Referral.get_referral("R001") is not None


def test_create_referral_flow_persists_to_file(capsys):
    create_referral_flow("R002", "CHP01", "H002")

    Referral.all_referrals = []
    Referral.load_from_file()
    assert Referral.get_referral("R002") is not None


def test_create_referral_flow_raises_on_missing_chp():
    with pytest.raises(ValueError):
        create_referral_flow("R003", None, "H003")


def test_list_referrals_flow_shows_referrals(capsys):
    create_referral_flow("R010", "CHP01", "H010")
    create_referral_flow("R011", "CHP01", "H011")

    list_referrals_flow("CHP01")

    captured = capsys.readouterr()
    assert "R010" in captured.out
    assert "R011" in captured.out


def test_list_referrals_flow_shows_message_when_none_found(capsys):
    list_referrals_flow("CHP-with-nothing")

    captured = capsys.readouterr()
    assert "no referrals found" in captured.out.lower()