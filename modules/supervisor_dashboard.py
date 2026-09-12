from modules.integration import Integration
from models.referral import Referral


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
        referrals = Referral.get_all_referrals()
        if not referrals:
            print("No referrals found.")
            return
        for referral in referrals:
            print(
                f"\nReferral ID: {referral.referral_id}\n"
                f"Household: {referral.household_id}\n"
                f"Reason: {referral.reason}\n"
                f"Status: {referral.status}"
            )

    def sync(self, chp_visits):
        success, message = self.integration.sync_visits(chp_visits)
        print(message)
        return success

    def update_referral(self, referral_id, status):
        referral = Referral.get_referral(referral_id)
        if not referral:
            print("Referral not found.")
            return False
        if status == "resolved":
            referral.resolve()
        elif status == "cancelled":
            referral.cancel()
        else:
            print("Invalid referral status")
            return False
        print("Referral status updated successfully")
        return True
