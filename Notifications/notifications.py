import sqlite3
from db import get_connection

class NotificationResult:
    def __init__(self, status, chp_id, referral_id):
        self.status = status
        self.chp_id = chp_id
        self.referral_id = referral_id


class NotificationService:
    def __init__(self, db_path):
        self.db_path = db_path

    def notify(self, referral_id, chp_id):
        self._validate(referral_id, chp_id)

        conn = get_connection(self.db_path)
        try:
            conn.execute(
                "INSERT INTO notifications (referral_id, chp_id) VALUES (?, ?)",
                (referral_id, chp_id),
            )
            conn.commit()
        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                raise ValueError(
                    f"Notification already sent for referral {referral_id}"
                ) from e
            if "FOREIGN KEY" in str(e):
                raise ValueError(
                    f"Referral {referral_id} does not exist"
                ) from e
            raise
        finally:
            conn.close()

        return NotificationResult(status="sent", chp_id=chp_id, referral_id=referral_id)

    def _validate(self, referral_id, chp_id):
        if not chp_id or not chp_id.strip():
            raise ValueError("chp_id is required")
        if not referral_id or not referral_id.strip():
            raise ValueError("referral_id is required")