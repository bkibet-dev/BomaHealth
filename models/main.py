from auth import Auth

if __name__ == "__main__":
    auth = Auth()
    while True:
        print("\n1. Register  2. Login  3. Profile  4. Change Password  5. Logout  0. Exit")
        c = input("> ").strip()
        if c == "0":
            break
        elif c == "1":
            s, m = auth.register(
                input("Name: "),
                input("Email: "),
                input("Phone: "),
                input("Password: "),
                input("Confirm password: ")
            )
            print(m)
        elif c == "2":
            s, m = auth.login(
                input("Email: "),
                input("Password: ")
            )
            print(m)
        elif c == "3":
            if auth.current_user:
                u = auth.current_user
                print(
                    f"Name: {u.name}\n"
                    f"Email: {u.email}\n"
                    f"Phone: {u.phone}\n"
                    f"Active: {u.is_active}"
                )
            else:
                print("Not logged in")
        elif c == "4":
            if auth.current_user:
                changed = auth.current_user.change_password(
                    input("Old Password: "),
                    input("New Password: ")
                )
                print("Changed" if changed else "Wrong PWD")
            else:
                print("Not logged in")
        elif c == "5":
            s, m = auth.logout()
            print(m)