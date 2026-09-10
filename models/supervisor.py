from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Supervisor:
    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self._password = generate_password_hash(password)
        self.created_date = datetime.now()
        self.is_active = True
    def verify_password(self, password):
        return check_password_hash(self._password, password)
    def change_password(self, old, new):
        if not self.verify_password(old):
            return False
        self._password = generate_password_hash(new)
        return True