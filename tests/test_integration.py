from modules.integration import Integration
from modules.chp_visit import CHPVisit

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
def test_get_referrals():
    integration = Integration()
    visit = CHPVisit("V001", "CHP01", "C001")
    visit.flag_referral(
        "R001",
        "Hospital",
        "Further assessment"
    )
    integration.sync_visits([visit])
    referrals = integration.get_referrals()
    assert len(referrals) == 1
    assert referrals[0]["referral_id"] == "R001"
def test_update_existing_visit():
    integration = Integration()
    visit1 = CHPVisit("V001", "CHP01", "C001")
    integration.sync_visits([visit1])
    visit2 = CHPVisit("V001", "CHP01", "C002")
    integration.sync_visits([visit2])
    visits = integration.get_visits()
    assert len(visits) == 1
    assert visits[0].client_id == "C002"