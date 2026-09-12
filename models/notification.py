import json
from datetime import datetime

from models.referral import Referral


class Notification:
    all_notifications = []

    def __init__(self, referral_id, chp_id, status="sent", sent_at=None):
        self.referral_id = referral_id
        self.chp_id = chp_id
        self.status = status
        self.sent_at = sent_at or datetime.now().isoformat()
        Notification.all_notifications.append(self)

    @classmethod
    def get_all_notifications(cls):
        return cls.all_notifications

    @classmethod
    def get_notification_for_referral(cls, referral_id):
        return next(
            (n for n in cls.all_notifications if n.referral_id == referral_id), None
        )

    @classmethod
    def notify(cls, referral_id, chp_id):
        if not chp_id or not str(chp_id).strip():
            raise ValueError("chp_id is required")
        if not referral_id or not str(referral_id).strip():
            raise ValueError("referral_id is required")
        if not Referral.get_referral(referral_id):
            raise ValueError(f"Referral {referral_id} does not exist")
        if cls.get_notification_for_referral(referral_id):
            raise ValueError(f"Notification already sent for referral {referral_id}")
        return cls(referral_id=referral_id, chp_id=chp_id)

    @classmethod
    def save_to_file(cls, filepath="data/notifications.json"):
        data = [
            {
                "referral_id": n.referral_id,
                "chp_id": n.chp_id,
                "status": n.status,
                "sent_at": n.sent_at,
            }
            for n in cls.all_notifications
        ]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, filepath="data/notifications.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            return
        cls.all_notifications = []
        for record in data:
            cls(
                referral_id=record["referral_id"],
                chp_id=record["chp_id"],
                status=record["status"],
                sent_at=record["sent_at"],
            )
            