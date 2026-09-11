from auth.decorators import requires_role

PRIORITY_ORDER = {"overdue": 0, "pending": 1, "visited": 2}
STATUS_COLORS = {"overdue": "\033[91m", "pending": "\033[93m", "visited": "\033[92m"}
RESET = "\033[0m"

def get_daily_list(chp):
    for household in chp.households:
        household.refresh_status()
    due_today = [h for h in chp.households if h.status != "visited"]
    due_today.sort(key=lambda h: (PRIORITY_ORDER[h.status], not h.priority))
    return due_today

@requires_role("chp")
def show_daily_planning(chp):
    households = get_daily_list(chp)
    if not households:
        print("No visits due today.")
        return
    print(f"Daily Plan for {chp.name}:")
    for h in households:
        color = STATUS_COLORS[h.status]
        flag = " [PRIORITY]" if h.priority else ""
        print(f"{color}[{h.status.upper()}]{RESET} {h.name}{flag}")