import pytest
from modules.integration import Integration
from modules.chp_visit import CHPVisit
from models.referral import Referral


@pytest.fixture(autouse=True)
def reset_referrals():
    Referral.all_referrals = []
    yield
    Referral.all_referrals = []


def test_sync_visit():
    integration = Integration()
    visit = CHPVisit("V001", "CHP01", "C001")
    success, message = integration.sync_visits([visit])
    assert success is True
    assert len(integration.get_visits()) == 1


def test_no_duplicate_visits():
    integration = Integration()
    visit = CHPVisit("V001", "CHP01", "C001")
    integration.sync_visits([visit])
    integration.sync_visits([visit])
    assert len(integration.get_visits()) == 1


def test_get_referrals_returns_referral_model_records():
    Referral.create_referral(referral_id="R001", chp_id="CHP01", household_id="H001")
    integration = Integration()
    referrals = integration.get_referrals()
    assert len(referrals) == 1
    assert referrals[0].referral_id == "R001"


def test_update_existing_visit():
    integration = Integration()
    visit1 = CHPVisit("V001", "CHP01", "C001")
    integration.sync_visits([visit1])
    visit2 = CHPVisit("V001", "CHP01", "C002")
    integration.sync_visits([visit2])
    visits = integration.get_visits()
    assert len(visits) == 1
    assert visits[0].client_id == "C002"
