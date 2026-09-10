from .integration import Integration

class SupervisorDashboard:
    def __init__(self, integration):
        self.integration = integration

    def show_visits(self):
        visits = self.integration.get_visits()
        if not visits:
            print("No CHP visits found.")
            return
        for visit in visits:
            print(
                f"\nVisit ID: {visit.visit_id}\n"
                f"CHP ID: {visit.chp_id}\n"
                f"Client ID: {visit.client_id}\n"
                f"Date: {visit.visit_date}\n"
                f"Notes: {visit.notes}"
            )
    def show_referrals(self):
        referrals = self.integration.get_referrals()
        if not referrals:
            print("No referrals found.")
            return
        for referral in referrals:
            print(
                f"\nReferral ID: {referral['referral_id']}\n"
                f"Referred To: {referral['referred_to']}\n"
                f"Reason: {referral['reason']}\n"
                f"Status: {referral['status']}"
            )
    def sync(self, chp_visits):
        success, message = self.integration.sync_visits(chp_visits)
        print(message)
        return success
    def update_referral(self, visit_id, status):
        visit = self.integration.visits.get(visit_id)

        if not visit:
            print("Visit not found.")
            return False
        success, message = visit.update_referral_status(status)
        print(message)
        return success