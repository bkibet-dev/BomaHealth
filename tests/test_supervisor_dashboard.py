from modules.integration import Integration
from modules.supervisor_dashboard import SupervisorDashboard
from modules.chp_visit import CHPVisit

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
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    visit = CHPVisit("V001", "CHP01", "C001")
    visit.flag_referral("R001", "Hospital", "Assessment")
    integration.sync_visits([visit])
    dashboard.show_referrals()
    assert "R001" in capsys.readouterr().out
def test_show_referrals_empty(capsys):
    dashboard = SupervisorDashboard(Integration())
    dashboard.show_referrals()
    assert "No referrals found." in capsys.readouterr().out
def test_update_referral():
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    visit = CHPVisit("V001", "CHP01", "C001")
    visit.flag_referral("R001", "Hospital", "Assessment")
    integration.sync_visits([visit])
    assert dashboard.update_referral("V001", "Completed") is True
def test_update_missing_visit():
    dashboard = SupervisorDashboard(Integration())
    assert dashboard.update_referral("V999", "Completed") is False
def test_update_without_referral():
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    integration.sync_visits([CHPVisit("V001", "CHP01", "C001")])
    assert dashboard.update_referral("V001", "Completed") is False
def test_sync():
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    assert dashboard.sync([
        CHPVisit("V001", "CHP01", "C001")
    ]) is True