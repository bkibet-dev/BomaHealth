from modules.auth import Auth

def test_register():
    auth = Auth()
    s, m = auth.register(
        "John", "john@test.com", "0712345678",
        "password", "password"
    )
    assert s is True
def test_duplicate_email():
    auth = Auth()
    auth.register(
        "John", "john@test.com", "0712345678",
        "password", "password"
    )
    s, m = auth.register(
        "Jane", "john@test.com", "0798765432",
        "password", "password"
    )
    assert s is False
def test_login():
    auth = Auth()
    auth.register(
        "John", "john@test.com", "0712345678",
        "password", "password"
    )
    s, m = auth.login("john@test.com", "password")
    assert s is True
def test_wrong_password():
    auth = Auth()
    auth.register(
        "John", "john@test.com", "0712345678",
        "password", "password"
    )
    s, m = auth.login("john@test.com", "wrong")
    assert s is False
def test_logout():
    auth = Auth()
    s, m = auth.logout()
    assert s is False