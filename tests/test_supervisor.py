from modules.supervisor import Supervisor

class TestSupervisor:
    def setup_method(self):
        self.sup = Supervisor(
            "John", "john@test.com", "0712345678", "password"
        )
    def test_details(self):
        assert self.sup.name == "John"
        assert self.sup.email == "john@test.com"
        assert self.sup.phone == "0712345678"
    def test_password_is_hashed(self):
        assert self.sup._password != "password"

    def test_correct_password(self):
        assert self.sup.verify_password("password") is True
    def test_wrong_password(self):
        assert self.sup.verify_password("wrong") is False
    def test_active_by_default(self):
        assert self.sup.is_active is True
    def test_change_password(self):
        success, message = self.sup.change_password(
            "password", "newpassword"
        )
        assert success is True
        assert self.sup.verify_password("newpassword") is True
    def test_wrong_old_password(self):
        success, message = self.sup.change_password(
            "wrong", "newpassword"
        )
        assert success is False
    def test_short_new_password(self):
        success, message = self.sup.change_password(
            "password", "123"
        )
        assert success is False