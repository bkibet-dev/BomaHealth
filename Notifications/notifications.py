from datetime import datetime
from store import JsonStore

class NotificationResult:
    def __init__(self, status, chp_id, referral_id):
        self.status = status
        self.chp_id = chp_id
        self.referral_id = referral_id

class NotificationService:
    def __init__(self, notifications_json_path, referrals_json_path):
        self.notifications = JsonStore(notifications_json_path)
        self.referrals = JsonStore(referrals_json_path)

    def notify(self, referral_id, chp_id):
        self._validate(referral_id, chp_id)

        if not self.referrals.exists(referral_id):
            raise ValueError(f"Referral {referral_id} does not exist")

        record = {
            "chp_id": chp_id,
            "status": "sent",
            "sent_at": datetime.now().isoformat(),
        }

        try:
            self.notifications.add_new(referral_id, record)
        except ValueError as e:
            raise ValueError(
                f"Notification already sent for referral {referral_id}"
            ) from e

        return NotificationResult(status="sent", chp_id=chp_id, referral_id=referral_id)

    def _validate(self, referral_id, chp_id):
        if not chp_id or not chp_id.strip():
            raise ValueError("chp_id is required")
        if not referral_id or not referral_id.strip():
            raise ValueError("referral_id is required")