from models.referral import Referral
from models.notification import Notification


def notify_flow(referral_id, chp_id):
    Referral.load_from_file()
    Notification.load_from_file()
    notification = Notification.notify(referral_id=referral_id, chp_id=chp_id)
    Notification.save_to_file()
    print(f"Notification sent to {notification.chp_id} for referral {notification.referral_id}")