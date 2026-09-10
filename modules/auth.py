from supervisor import Supervisor

class Auth:
    def __init__(self):
        self.supervisors = {}
        self.current_user = None
    def register(self, name, email, phone, pwd, confirm):
        name = name.strip()
        email = email.strip().lower()
        phone = phone.strip()
        if not name:
            return False, "Name required"
        if not email:
            return False, "Email cannot be empty"
        if not phone:
            return False, "Phone required"
        if not pwd:
            return False, "Password required"
        if email in self.supervisors:
            return False, "Email already registered"
        if len(pwd) < 6:
            return False, "Password must be at least 6 characters"
        if pwd != confirm:
            return False, "Passwords do not match"
        self.supervisors[email] = Supervisor(name, email, phone, pwd)
        return True, f"{name} registered successfully"
    def login(self, email, pwd):
        email = email.strip().lower()
        if not email:
            return False, "Email required"
        if not pwd:
            return False, "Password required"
        if email not in self.supervisors:
            return False, "Email not found"
        sup = self.supervisors[email]
        if not sup.verify_password(pwd):
            return False, "Wrong password"
        if not sup.is_active:
            return False, "Account is inactive"
        self.current_user = sup
        return True, f"Welcome, {sup.name}"
    def logout(self):
        if self.current_user:
            name = self.current_user.name
            self.current_user = None
            return True, f"Goodbye, {name}"
        return False, "Not logged in"