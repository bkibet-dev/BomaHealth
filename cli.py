import functools

from Referrals import ReferralService
from Notifications import NotificationService


def handle_errors(flow_fn):
    @functools.wraps(flow_fn)
    def wrapper(*args, **kwargs):
        try:
            flow_fn(*args, **kwargs)
        except ValueError as e:
            print(f"⚠️  {e}")

    return wrapper


@handle_errors
def create_referral_flow(referral_service):
    print("\n-- New Referral --")
    referral_id = input("Referral ID: ").strip()
    chp_id = input("CHP ID: ").strip()
    household_id = input("Household ID: ").strip()
    reason = input("Reason (optional): ").strip() or None

    result = referral_service.create_referral(
        referral_id=referral_id, chp_id=chp_id, household_id=household_id, reason=reason
    )
    print(f"✅ Referral {result.referral_id} created (status: {result.status})")


@handle_errors
def list_referrals_flow(referral_service):
    chp_id = input("\nList referrals for CHP ID: ").strip()
    referrals = referral_service.list_referrals_for_chp(chp_id)

    if not referrals:
        print("No referrals found for this CHP.")
        return

    referrals = sorted(referrals, key=lambda r: r.created_at, reverse=True)
    for r in referrals:
        print(f"  [{r.status.upper()}] {r.referral_id} — {r.household_id} ({r.created_at})")


@handle_errors
def notify_flow(notification_service):
    print("\n-- Send Notification --")
    referral_id = input("Referral ID: ").strip()
    chp_id = input("CHP ID: ").strip()

    result = notification_service.notify(referral_id=referral_id, chp_id=chp_id)
    print(f"✅ Notification sent to {result.chp_id} for referral {result.referral_id}")


def print_menu():
    print("\n===== BomaHealth =====")
    print("1. Create referral")
    print("2. List referrals for a CHP")
    print("3. Send notification for a referral")
    print("0. Exit")


def run_menu(referrals_json_path, notifications_json_path, role=None):
    referral_service = ReferralService(referrals_json_path)
    notification_service = NotificationService(notifications_json_path, referrals_json_path)

    while True:
        print_menu()
        choice = input("> ").strip()

        action = {
            "1": lambda: create_referral_flow(referral_service),
            "2": lambda: list_referrals_flow(referral_service),
            "3": lambda: notify_flow(notification_service),
        }.get(choice, None)

        if choice == "0":
            print("Goodbye.")
            break
        elif action:
            action()
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    run_menu("referrals.json", "notifications.json")