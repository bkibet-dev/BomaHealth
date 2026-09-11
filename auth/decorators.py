from functools import wraps

def requires_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(current_user, *args, **kwargs):
            if current_user.role not in allowed_roles:
                print(f"Access denied: requires role {allowed_roles}")
                return None
            return func(current_user, *args, **kwargs)
        return wrapper
    return decorator