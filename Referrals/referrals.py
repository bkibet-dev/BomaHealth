from datetime import datetime

from store import JsonStore


class ReferralResult:
    def __init__(self, referral_id, chp_id, household_id, reason, status, created_at):
        self.referral_id = referral_id
        self.chp_id = chp_id
        self.household_id = household_id
        self.reason = reason
        self.status = status
        self.created_at = created_at

    @classmethod
    def _from_dict(cls, referral_id, d):
        return cls(
            referral_id=referral_id,
            chp_id=d["chp_id"],
            household_id=d["household_id"],
            reason=d.get("reason"),
            status=d["status"],
            created_at=d["created_at"],
        )


class ReferralService:
    def __init__(self, json_path):
        self.store = JsonStore(json_path)

    def create_referral(self, referral_id, chp_id, household_id, reason=None):
        self._validate(referral_id, chp_id, household_id)

        record = {
            "chp_id": chp_id,
            "household_id": household_id,
            "reason": reason,
            "status": "open",
            "created_at": datetime.now().isoformat(),
        }

        try:
            self.store.add_new(referral_id, record)
        except ValueError as e:
            raise ValueError(f"Referral {referral_id} already exists") from e

        return self.get_referral(referral_id)

    def get_referral(self, referral_id):
        record = self.store.get(referral_id)
        return ReferralResult._from_dict(referral_id, record) if record else None

    def list_referrals_for_chp(self, chp_id):
        all_referrals = self.store.get_all()
        # comprehension, per the OOP-tricks requirement
        return [
            ReferralResult._from_dict(rid, r)
            for rid, r in all_referrals.items()
            if r["chp_id"] == chp_id
        ]

    def _validate(self, referral_id, chp_id, household_id):
        if not referral_id or not referral_id.strip():
            raise ValueError("referral_id is required")
        if not chp_id or not chp_id.strip():
            raise ValueError("chp_id is required")
        if not household_id or not household_id.strip():
            raise ValueError("household_id is required")