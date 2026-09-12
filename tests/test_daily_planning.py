from datetime import date, timedelta
from models.household import Household
from models.person import CHP
from cli.daily_planning import get_daily_list, show_daily_planning

def make_chp():
    Household.all_households = []
    return CHP("Test CHP", 1)
def test_overdue_sorted_before_pending():
    chp = make_chp()
    a = Household("A", "H001", chp_id=1)
    b = Household("B", "H002", chp_id=1, last_visit_date=date.today() - timedelta(days=10))
    b.status = "visited"
    chp.add_household(a)
    chp.add_household(b)
    result = get_daily_list(chp)
    assert result[0].name == "B"
def test_visited_excluded_from_list():
    chp = make_chp()
    h = Household("C", "H003", chp_id=1)
    h.mark_visited()
    chp.add_household(h)
    assert get_daily_list(chp) == []
def test_empty_list_returns_empty():
    chp = make_chp()
    assert get_daily_list(chp) == []
def test_priority_household_ranked_first_among_pending():
    chp = make_chp()
    old_visit = date.today() - timedelta(days=3)
    a = Household("A", "H004", chp_id=1, last_visit_date=old_visit)
    b = Household("B", "H005", chp_id=1)
    chp.add_household(a)
    chp.add_household(b)
    result = get_daily_list(chp)
    assert result[0].name == "B"
def test_show_daily_planning_empty_state(capsys):
    chp = make_chp()
    show_daily_planning(chp)
    captured = capsys.readouterr()
    assert "No visits due today." in captured.out
def test_show_daily_planning_prints_list(capsys):
    chp = make_chp()
    h = Household("Wanjiku", "H001", chp_id=1)
    chp.add_household(h)
    show_daily_planning(chp)
    captured = capsys.readouterr()
    assert "Wanjiku" in captured.out
def test_show_daily_planning_denies_wrong_role(capsys):
    class FakeSupervisor:
        role = "supervisor"
        name = "Fake Sup"
        households = []
    show_daily_planning(FakeSupervisor())
    captured = capsys.readouterr()
    assert "Access denied" in captured.out