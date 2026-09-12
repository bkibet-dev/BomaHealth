import os
from datetime import date, timedelta
from models.household import Household

def test_new_household_defaults_to_priority():
    h = Household("Wanjiku", "H001", chp_id=1)
    assert h.priority is True
    assert h.status == "pending"
def test_mark_visited_updates_status_and_date():
    h = Household("Wanjiku", "H002", chp_id=1)
    h.mark_visited()
    assert h.status == "visited"
    assert h.last_visit_date == date.today()
    assert h.priority is False
def test_becomes_overdue_after_threshold():
    old_date = date.today() - timedelta(days=Household.overdue_threshold_days + 1)
    h = Household("Wanjiku", "H003", chp_id=1, last_visit_date=old_date)
    h.status = "visited"
    h.refresh_status()
    assert h.status == "overdue"
    assert h.priority is True
def test_recently_visited_not_overdue():
    recent = date.today() - timedelta(days=1)
    h = Household("Wanjiku", "H004", chp_id=1, last_visit_date=recent)
    h.status = "visited"
    h.refresh_status()
    assert h.status == "visited"
def test_reassign_changes_chp():
    h = Household("Wanjiku", "H005", chp_id=1)
    h.reassign(2)
    assert h.chp_id == 2
def test_get_households_for_chp():
    Household.all_households = []
    h1 = Household("A", "H006", chp_id=5)
    h2 = Household("B", "H007", chp_id=6)
    result = Household.get_households_for_chp(5)
    assert result == [h1]
def test_get_all_people_via_person():
    from models.person import Person
    Person.all_people = []
    p = Person("Test", 1, "chp")
    assert Person.get_all_people() == [p]
def test_save_to_file_creates_json(tmp_path):
    Household.all_households = []
    h = Household("Wanjiku", "H001", chp_id=1)
    filepath = tmp_path / "households.json"
    Household.save_to_file(filepath=str(filepath))
    assert os.path.exists(filepath)
def test_load_from_file_restores_households(tmp_path):
    Household.all_households = []
    h = Household("Wanjiku", "H001", chp_id=1)
    h.mark_visited()
    filepath = tmp_path / "households.json"
    Household.save_to_file(filepath=str(filepath))
    Household.all_households = []
    Household.load_from_file(filepath=str(filepath))
    loaded = Household.get_all_households()
    assert len(loaded) == 1
    assert loaded[0].name == "Wanjiku"
    assert loaded[0].status == "visited"
def test_load_from_file_missing_file_does_not_crash(tmp_path):
    Household.all_households = []
    filepath = tmp_path / "does_not_exist.json"
    Household.load_from_file(filepath=str(filepath))
    assert Household.get_all_households() == []