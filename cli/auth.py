"""CLI functions for registration/login, mirrors the pattern in
cli/referrals.py and cli/notifications.py."""

from modules.auth import Auth


def register_flow(name, email, phone, password, confirm):
    auth = Auth()
    success, message = auth.register(name, email, phone, password, confirm)
    print(message)
    return success


def login_flow(email, password):
    auth = Auth()
    success, message = auth.login(email, password)
    print(message)
    return success
