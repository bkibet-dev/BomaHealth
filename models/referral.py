import json
from datetime import datetime


class Referral:
    all_referrals = []

    def __init__(self, referral_id, chp_id, household_id, reason=None,
                 status="open", created_at=None):
        self.referral_id = referral_id
        self.chp_id = chp_id
        self.household_id = household_id
        self.reason = reason
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        Referral.all_referrals.append(self)

    @classmethod
    def get_all_referrals(cls):
        return cls.all_referrals

    @classmethod
    def get_referrals_for_chp(cls, chp_id):
        return [r for r in cls.all_referrals if r.chp_id == chp_id]

    @classmethod
    def get_referral(cls, referral_id):
        return next((r for r in cls.all_referrals if r.referral_id == referral_id), None)

    @classmethod
    def create_referral(cls, referral_id, chp_id, household_id, reason=None):
        if not referral_id or not str(referral_id).strip():
            raise ValueError("referral_id is required")
        if not chp_id or not str(chp_id).strip():
            raise ValueError("chp_id is required")
        if not household_id or not str(household_id).strip():
            raise ValueError("household_id is required")
        if cls.get_referral(referral_id):
            raise ValueError(f"Referral {referral_id} already exists")
        return cls(referral_id=referral_id, chp_id=chp_id, household_id=household_id, reason=reason)

    def resolve(self):
        self.status = "resolved"

    def cancel(self):
        self.status = "cancelled"

    @classmethod
    def save_to_file(cls, filepath="data/referrals.json"):
        data = [
            {
                "referral_id": r.referral_id,
                "chp_id": r.chp_id,
                "household_id": r.household_id,
                "reason": r.reason,
                "status": r.status,
                "created_at": r.created_at,
            }
            for r in cls.all_referrals
        ]
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, filepath="data/referrals.json"):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            return
        cls.all_referrals = []
        for record in data:
            cls(
                referral_id=record["referral_id"],
                chp_id=record["chp_id"],
                household_id=record["household_id"],
                reason=record.get("reason"),
                status=record["status"],
                created_at=record["created_at"],
            )