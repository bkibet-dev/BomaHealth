from models.referral import Referral


class Integration:
    def __init__(self):
        self.visits = {}

    def sync_visits(self, chp_visits):
        added = 0
        updated = 0
        for visit in chp_visits:
            visit_id = visit.visit_id
            if visit_id in self.visits:
                self.visits[visit_id] = visit
                updated += 1
            else:
                self.visits[visit_id] = visit
                added += 1
        return True, f"Sync complete: {added} added, {updated} updated"

    def get_visits(self):
        return list(self.visits.values())

    def get_referrals(self):
        return Referral.get_all_referrals()
