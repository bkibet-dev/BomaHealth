from supervisor import Supervisor

class Auth:
    def __init__(self):
        self.supervisors = {}
        self.current_user = None
    def register(self, name, email, phone, pwd, confirm):
        if email in self.supervisors or pwd != confirm or len(pwd) < 6:
            return False, "Invalid"
        self.supervisors[email] = Supervisor(name, email, phone, pwd)
        return True, f"{name} registered"
    def login(self, email, pwd):
        if email not in self.supervisors:
            return False, "Not found"
        sup = self.supervisors[email]
        if not sup.verify_password(pwd):
            return False, "Wrong password"
        self.current_user = sup
        return True, f"Welcome, {sup.name}"
    def logout(self):
        if self.current_user:
            name = self.current_user.name
            self.current_user = None
            return True, f"Goodbye, {name}"
        return False, "Not logged in"