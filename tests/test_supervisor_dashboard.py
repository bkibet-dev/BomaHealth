import pytest
from modules.integration import Integration
from modules.supervisor_dashboard import SupervisorDashboard
from modules.chp_visit import CHPVisit
from models.referral import Referral


@pytest.fixture(autouse=True)
def reset_referrals():
    Referral.all_referrals = []
    yield
    Referral.all_referrals = []


def test_show_visits():
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    visit = CHPVisit("V001", "CHP01", "C001", notes="Routine")
    integration.sync_visits([visit])
    dashboard.show_visits()
    assert integration.get_visits()[0].visit_id == "V001"


def test_show_visits_empty(capsys):
    dashboard = SupervisorDashboard(Integration())
    dashboard.show_visits()
    assert "No CHP visits found." in capsys.readouterr().out


def test_show_referrals(capsys):
    Referral.create_referral(referral_id="R001", chp_id="CHP01", household_id="H001", reason="Assessment")
    dashboard = SupervisorDashboard(Integration())
    dashboard.show_referrals()
    assert "R001" in capsys.readouterr().out


def test_show_referrals_empty(capsys):
    dashboard = SupervisorDashboard(Integration())
    dashboard.show_referrals()
    assert "No referrals found." in capsys.readouterr().out


def test_update_referral_resolves_successfully():
    Referral.create_referral(referral_id="R001", chp_id="CHP01", household_id="H001")
    dashboard = SupervisorDashboard(Integration())
    assert dashboard.update_referral("R001", "resolved") is True
    assert Referral.get_referral("R001").status == "resolved"


def test_update_referral_missing_referral():
    dashboard = SupervisorDashboard(Integration())
    assert dashboard.update_referral("R999", "resolved") is False


def test_update_referral_invalid_status():
    Referral.create_referral(referral_id="R001", chp_id="CHP01", household_id="H001")
    dashboard = SupervisorDashboard(Integration())
    assert dashboard.update_referral("R001", "not-a-status") is False


def test_sync():
    dashboard = SupervisorDashboard(Integration())
    assert dashboard.sync([
        CHPVisit("V001", "CHP01", "C001")
    ]) is True
