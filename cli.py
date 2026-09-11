import functools

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from Referrals import ReferralService
from Notifications import NotificationService

NAVY = "#2F4156"
TEAL = "#567C8D"
BEIGE = "#F5EFEB"
SKY_BLUE = "#C8D9E6"
WHITE = "#FFFFFF"

console = Console()


def handle_errors(flow_fn):
    @functools.wraps(flow_fn)
    def wrapper(*args, **kwargs):
        try:
            flow_fn(*args, **kwargs)
        except ValueError as e:
            console.print(f"⚠️  {e}", style="bold red")

    return wrapper


@handle_errors
def create_referral_flow(referral_service):
    console.print("\n-- New Referral --", style=f"bold {NAVY}")
    referral_id = input("Referral ID: ").strip()
    chp_id = input("CHP ID: ").strip()
    household_id = input("Household ID: ").strip()
    reason = input("Reason (optional): ").strip() or None

    result = referral_service.create_referral(
        referral_id=referral_id, chp_id=chp_id, household_id=household_id, reason=reason
    )
    console.print(
        f"✅ Referral {result.referral_id} created (status: {result.status})",
        style=f"bold {TEAL}",
    )


@handle_errors
def list_referrals_flow(referral_service):
    chp_id = input("\nList referrals for CHP ID: ").strip()
    referrals = referral_service.list_referrals_for_chp(chp_id)

    if not referrals:
        console.print("No referrals found for this CHP.", style=SKY_BLUE)
        return

    referrals = sorted(referrals, key=lambda r: r.created_at, reverse=True)

    table = Table(title=f"Referrals for {chp_id}", border_style=NAVY, header_style=f"bold {TEAL}")
    table.add_column("Referral ID")
    table.add_column("Household")
    table.add_column("Status")
    table.add_column("Created At")

    for r in referrals:
        table.add_row(r.referral_id, r.household_id, r.status.upper(), r.created_at)

    console.print(table)


@handle_errors
def notify_flow(notification_service):
    console.print("\n-- Send Notification --", style=f"bold {NAVY}")
    referral_id = input("Referral ID: ").strip()
    chp_id = input("CHP ID: ").strip()

    result = notification_service.notify(referral_id=referral_id, chp_id=chp_id)
    console.print(
        f"✅ Notification sent to {result.chp_id} for referral {result.referral_id}",
        style=f"bold {TEAL}",
    )


def print_menu():
    menu_text = (
        "[bold]1.[/bold] Create referral\n"
        "[bold]2.[/bold] List referrals for a CHP\n"
        "[bold]3.[/bold] Send notification for a referral\n"
        "[bold]0.[/bold] Exit"
    )
    console.print(Panel(menu_text, title="BomaHealth", border_style=NAVY, style=WHITE))


def run_menu(referrals_json_path, notifications_json_path, role=None):
    """Main CLI loop. `role` is accepted now so RBAC can be wired in
    later without changing this function's signature — currently
    unused (no gating applied) until the auth feature is merged."""
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
            console.print("Goodbye.", style=TEAL)
            break
        elif action:
            action()
        else:
            console.print("Invalid option, try again.", style="bold red")


if __name__ == "__main__":
    run_menu("referrals.json", "notifications.json")