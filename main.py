import argparse
from models.person import CHP
from cli.daily_planning import show_daily_planning

def build_parser():
    parser = argparse.ArgumentParser(prog="chp-companion")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("daily-plan", help="Show today's prioritized household list")
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "daily-plan":
        chp = CHP()
        show_daily_planning(chp)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()