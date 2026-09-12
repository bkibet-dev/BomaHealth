# BomaHealth

A Python OOP command-line application for tracking household visits and referrals in Kenya's Community Health Promoter (CHP) system. Built as a summative group lab project.

## Overview

BomaHealth helps Community Health Promoters (CHPs) and their Supervisors manage day-to-day fieldwork: tracking household visits, flagging referrals that need follow-up, sending notifications, and reviewing progress — all from a simple command-line tool, with no database server required.

**Team:** Brandon Kibet, Patience Savera, Flavia Kihahu

## Features

- **Household tracking** — register households, mark visits complete, auto-flag overdue follow-ups
- **Referrals** — create referrals tied to a household and CHP, track status (open/resolved/cancelled)
- **Notifications** — notify a CHP when a referral is created, with duplicate-notification prevention
- **Daily planning** — a prioritized, color-coded list of a CHP's households due for a visit today
- **Supervisor dashboard** — view visits and referrals across CHPs, update referral status
- **Authentication** — registration and login with hashed passwords, role-based access (CHP / Supervisor)
- **JSON persistence** — no database setup needed; each model saves to and loads from its own JSON file

## Requirements

- Python 3.12+
- pip

## Installation

```bash
git clone https://github.com/bkibet-dev/BomaHealth.git
cd BomaHealth
pip install -r requirements.txt
```

## Usage

Run commands via `main.py`:

```bash
# Show today's prioritized household list for a CHP
python main.py daily-plan

# Create a referral
python main.py create-referral --referral-id R001 --chp CHP01 --household H001 --reason "Fever"

# List referrals for a CHP
python main.py list-referrals --chp CHP01

# Send a notification for an existing referral
python main.py notify --referral-id R001 --chp CHP01
```

Run `python main.py --help` to see all available commands.

## Project Structure

```
BomaHealth/
├── auth/               # Role-based access control decorators
├── cli/                # CLI-facing functions, one module per feature
├── models/             # Domain classes (Household, Person, Referral, Notification)
├── modules/            # Business logic (auth, visits, supervisor, storage helpers)
├── data/               # JSON data files (git-ignored)
├── tests/              # Test suite (pytest)
├── main.py             # CLI entry point (argparse)
├── requirements.txt
└── pytest.ini
```

Each domain model (e.g. `Referral`, `Notification`, `Household`) manages its own in-memory list and its own `save_to_file` / `load_from_file` methods — there's no shared database layer.

## Testing

This project follows Test-Driven Development (TDD). Run the full suite with:

```bash
pytest -v
```

Coverage is enforced at a 90% minimum (configured in `pytest.ini`):

```bash
pytest --cov-report=term-missing
```

## Git Workflow

- `main` — production-ready code only
- `development` — default branch; all feature work is reviewed and merged here
- Working branches follow `<type>/<short-description>`:
  - `feat/` or `ft/` — new functionality
  - `bf/` — bug fixes
  - `ch/` — chores (config, maintenance, non-feature changes)
  - `hotfix/` — urgent fixes pushed directly to `main`

**Pull requests** are opened against `development`, titled as a user story, and must describe: what the PR does, what task it completes, and how to manually test it. All merges are **squashed** and reviewed/merged by the Scrum Master. Branches are deleted once merged.

## Contributing

See the branch naming and PR conventions above. Before starting new work:

```bash
git checkout development
git pull
git checkout -b feat/short-description
```