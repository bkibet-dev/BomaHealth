from modules.integration import Integration
from modules.supervisor_dashboard import SupervisorDashboard
from modules.chp_visit import CHPVisit

def test_show_visits():
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    visit = CHPVisit("V001", "CHP01", "C001", notes="Routine visit")
    integration.sync_visits([visit])
    visits = integration.get_visits()
    assert len(visits) == 1
    assert visits[0].visit_id == "V001"
def test_show_referrals():
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    visit = CHPVisit("V001", "CHP01", "C001")
    visit.flag_referral("R001", "Hospital", "Further assessment")
    integration.sync_visits([visit])
    referrals = integration.get_referrals()    
    assert len(referrals) == 1
    assert referrals[0]["referral_id"] == "R001"
def test_update_referral():
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    visit = CHPVisit("V001", "CHP01", "C001")
    visit.flag_referral("R001", "Hospital", "Further assessment")
    integration.sync_visits([visit])
    success = dashboard.update_referral(
        "V001", "Completed"
    )
    assert success is True
    assert visit.referral["status"] == "Completed"
def test_update_missing_visit():
    integration = Integration()
    dashboard = SupervisorDashboard(integration)

    success = dashboard.update_referral(
        "V999", "Completed"
    )
    assert success is False