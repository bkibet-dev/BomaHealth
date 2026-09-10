from datetime import datetime

class CHPVisit:
    def __init__(
        self,
        visit_id,
        chp_id,
        client_id,
        visit_date=None,
        notes=""
    ):
        self.visit_id = visit_id
        self.chp_id = chp_id
        self.client_id = client_id
        self.visit_date = visit_date or datetime.now()
        self.notes = notes
        self.referral = None
    def flag_referral(self, referral_id, referred_to, reason):
        self.referral = {
            "referral_id": referral_id,
            "referred_to": referred_to,
            "reason": reason,
            "status": "Pending",
            "created_date": datetime.now()
        }
    def update_referral_status(self, status):
        if self.referral is None:
            return False, "No referral has been flagged"
        allowed_statuses = [
            "Pending",
            "Completed",
            "Cancelled"
        ]

        if status not in allowed_statuses:
            return False, "Invalid referral status"
        self.referral["status"] = status
        return True, "Referral status updated successfully"