import sqlite3

from db import get_connection


class ReferralResult:
    def __init__(self, referral_id, chp_id, household_id, reason, status, created_at):
        self.referral_id = referral_id
        self.chp_id = chp_id
        self.household_id = household_id
        self.reason = reason
        self.status = status
        self.created_at = created_at

    @classmethod
    def _from_row(cls, row):
        return cls(
            referral_id=row["referral_id"],
            chp_id=row["chp_id"],
            household_id=row["household_id"],
            reason=row["reason"],
            status=row["status"],
            created_at=row["created_at"],
        )


class ReferralService:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_referral(self, referral_id, chp_id, household_id, reason=None):
        self._validate(referral_id, chp_id, household_id)

        conn = get_connection(self.db_path)
        try:
            conn.execute(
                "INSERT INTO referrals (referral_id, chp_id, household_id, reason) "
                "VALUES (?, ?, ?, ?)",
                (referral_id, chp_id, household_id, reason),
            )
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Referral {referral_id} already exists") from e
        finally:
            conn.close()

        return self.get_referral(referral_id)

    def get_referral(self, referral_id):
        conn = get_connection(self.db_path)
        try:
            row = conn.execute(
                "SELECT * FROM referrals WHERE referral_id = ?", (referral_id,)
            ).fetchone()
        finally:
            conn.close()

        return ReferralResult._from_row(row) if row else None

    def list_referrals_for_chp(self, chp_id):
        conn = get_connection(self.db_path)
        try:
            rows = conn.execute(
                "SELECT * FROM referrals WHERE chp_id = ?", (chp_id,)
            ).fetchall()
        finally:
            conn.close()

        return [ReferralResult._from_row(row) for row in rows]

    def _validate(self, referral_id, chp_id, household_id):
        if not referral_id or not referral_id.strip():
            raise ValueError("referral_id is required")
        if not chp_id or not chp_id.strip():
            raise ValueError("chp_id is required")
        if not household_id or not household_id.strip():
            raise ValueError("household_id is required")