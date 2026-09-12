import json
from datetime import date

class Household:
    all_households = []
    overdue_threshold_days = 7
    def __init__(self, name, household_no, chp_id, last_visit_date=None):
        self.name = name
        self.household_no = household_no
        self.chp_id = chp_id
        self.last_visit_date = last_visit_date
        self.priority = last_visit_date is None
        self.status = "pending"
        Household.all_households.append(self)
    @classmethod
    def get_all_households(cls):
        return cls.all_households
    @classmethod
    def get_households_for_chp(cls, chp_id):
        return [h for h in cls.all_households if h.chp_id == chp_id]
    def mark_visited(self):
        self.status = "visited"
        self.last_visit_date = date.today()
        self.priority = False
    def refresh_status(self):
        if self.status == "visited" and self.last_visit_date:
            days_since = (date.today() - self.last_visit_date).days
            if days_since > Household.overdue_threshold_days:
                self.status = "overdue"
                self.priority = True
    def reassign(self, new_chp_id):
        self.chp_id = new_chp_id
    @classmethod
    def save_to_file(cls, filepath="data/households.json"):
        data = []
        for h in cls.all_households:
            data.append({
                "name": h.name,
                "household_no": h.household_no,
                "chp_id": h.chp_id,
                "last_visit_date": h.last_visit_date.isoformat() if h.last_visit_date else None,
                "status": h.status,
                "priority": h.priority,
            })
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    @classmethod
    def load_from_file(cls, filepath="data/households.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            return
        cls.all_households = []
        for record in data:
            h = cls(record["name"], record["household_no"], record["chp_id"])
            h.status = record["status"]
            h.priority = record["priority"]
            if record["last_visit_date"]:
                h.last_visit_date = date.fromisoformat(record["last_visit_date"])
if __name__ == "__main__":
    h1 = Household("Wanjiku", "H001", chp_id=1)
    print(h1.status)
    h1.mark_visited()
    print(h1.status)
    print(Household.get_all_households())
