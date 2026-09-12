from modules.chp_visit import CHPVisit


def test_create_visit():
    visit = CHPVisit("V001", "CHP01", "C001")

    assert visit.visit_id == "V001"
    assert visit.chp_id == "CHP01"
    assert visit.client_id == "C001"


def test_flag_referral():
    visit = CHPVisit("V001", "CHP01", "C001")

    visit.flag_referral(
        "R001",
        "Hospital",
        "Further assessment"
    )

    assert visit.referral["referral_id"] == "R001"
    assert visit.referral["status"] == "Pending"


def test_update_referral_status():
    visit = CHPVisit("V001", "CHP01", "C001")

    visit.flag_referral(
        "R001",
        "Hospital",
        "Further assessment"
    )

    success, message = visit.update_referral_status("Completed")

    assert success is True
    assert visit.referral["status"] == "Completed"


def test_invalid_referral_status():
    visit = CHPVisit("V001", "CHP01", "C001")

    visit.flag_referral(
        "R001",
        "Hospital",
        "Further assessment"
    )

    success, message = visit.update_referral_status("Invalid")

    assert success is False