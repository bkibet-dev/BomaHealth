from modules.auth import Auth

def test_register():
    auth = Auth()
    assert auth.register(
        "John", "john@example.com", "0712345678",
        "password", "password"
    )[0] is False
def test_duplicate_email():
    auth = Auth()
    auth.register(
        "John", "john@example.com", "0712345678",
        "password", "password"
    )
    assert auth.register(
        "Jane", "john@example.com", "0798765432",
        "password", "password"
    )[0] is False
def test_login():
    auth = Auth()
    auth.register(
        "John", "john@example.com", "0712345678",
        "password", "password"
    )
    assert auth.login("john@example.com", "password")[0] is True
def test_wrong_password():
    auth = Auth()
    auth.register(
        "John", "john@example.com", "0712345678",
        "password", "password"
    )
    assert auth.login("john@example.com", "wrong")[0] is False
def test_logout():
    assert Auth().logout()[0] is False
def test_register_validation():
    auth = Auth()
    assert auth.register("", "test@test.com", "0712345678", "password", "password")[0] is False
    assert auth.register("John", "", "0712345678", "password", "password")[0] is False
    assert auth.register("John", "test@test.com", "", "password", "password")[0] is False
    assert auth.register("John", "test@test.com", "0712345678", "", "")[0] is False
    assert auth.register("John", "test@test.com", "0712345678", "123", "123")[0] is False
    assert auth.register("John", "test@test.com", "0712345678", "password", "wrong")[0] is False
def test_login_validation():
    auth = Auth()
    assert auth.login("", "password")[0] is False
    assert auth.login("missing@test.com", "password")[0] is False
    auth.register("John", "login@test.com", "0712345678", "password", "password")
    assert auth.login("login@test.com", "")[0] is False
def test_logout_logged_in():
    auth = Auth()
    auth.register("John", "logout@test.com", "0712345678", "password", "password")
    auth.login("logout@test.com", "password")
    assert auth.logout()[0] is True
def test_inactive_account():
    auth = Auth()
    auth.register("John", "inactive@test.com", "0712345678", "password", "password")
    auth.supervisors["inactive@test.com"].is_active = False
    assert auth.login("inactive@test.com", "password")[0] is False