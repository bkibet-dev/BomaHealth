import argparse
from models.person import CHP
from models.household import Household
from cli.daily_planning import show_daily_planning
from cli.referrals import create_referral_flow, list_referrals_flow
from cli.notifications import notify_flow
from cli.auth import register_flow, login_flow

def build_parser():
    parser = argparse.ArgumentParser(prog="chp-companion")
    subparsers = parser.add_subparsers(dest="command")

    daily_plan = subparsers.add_parser("daily-plan", help="Show today's prioritized household list")
    daily_plan.add_argument("--name", required=True)
    daily_plan.add_argument("--chp", required=True)

    register = subparsers.add_parser("register", help="Register a new supervisor account")
    register.add_argument("--name", required=True)
    register.add_argument("--email", required=True)
    register.add_argument("--phone", required=True)
    register.add_argument("--password", required=True)
    register.add_argument("--confirm", required=True)

    login = subparsers.add_parser("login", help="Log in as a supervisor")
    login.add_argument("--email", required=True)
    login.add_argument("--password", required=True)

    create_ref = subparsers.add_parser("create-referral", help="Create a new referral")
    create_ref.add_argument("--referral-id", required=True)
    create_ref.add_argument("--chp", required=True)
    create_ref.add_argument("--household", required=True)
    create_ref.add_argument("--reason")

    list_ref = subparsers.add_parser("list-referrals", help="List referrals for a CHP")
    list_ref.add_argument("--chp", required=True)

    notify = subparsers.add_parser("notify", help="Send a notification for a referral")
    notify.add_argument("--referral-id", required=True)
    notify.add_argument("--chp", required=True)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "daily-plan":
        Household.load_from_file()
        chp = CHP(args.name, args.chp)
        for h in Household.get_households_for_chp(args.chp):
            chp.add_household(h)
        show_daily_planning(chp)
    elif args.command == "register":
        register_flow(args.name, args.email, args.phone, args.password, args.confirm)
    elif args.command == "login":
        login_flow(args.email, args.password)
    elif args.command == "create-referral":
        create_referral_flow(args.referral_id, args.chp, args.household, args.reason)
    elif args.command == "list-referrals":
        list_referrals_flow(args.chp)
    elif args.command == "notify":
        notify_flow(args.referral_id, args.chp)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()