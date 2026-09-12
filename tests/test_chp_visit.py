from modules.chp_visit import CHPVisit


def test_create_visit():
    visit = CHPVisit("V001", "CHP01", "C001")

    assert visit.visit_id == "V001"
    assert visit.chp_id == "CHP01"
    assert visit.client_id == "C001"


def test_create_visit_defaults_notes_to_empty_string():
    visit = CHPVisit("V002", "CHP01", "C002")
    assert visit.notes == ""


def test_create_visit_with_notes():
    visit = CHPVisit("V003", "CHP01", "C003", notes="Follow-up needed")
    assert visit.notes == "Follow-up needed"
