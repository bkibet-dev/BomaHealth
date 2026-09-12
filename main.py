import argparse
from models.person import CHP
from cli.daily_planning import show_daily_planning
from cli.referrals import create_referral_flow, list_referrals_flow
from cli.notifications import notify_flow

def build_parser():
    parser = argparse.ArgumentParser(prog="chp-companion")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("daily-plan", help="Show today's prioritized household list")

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
        chp = CHP()
        show_daily_planning(chp)
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