from auth import Auth

if __name__ == "__main__":
    auth = Auth()
    while True:
        try:
            print("\n1. Register  2. Login  3. Profile  4. Change PWD  5. Logout  0. Exit")
            c = input("> ").strip()
            if c == "0":
                print("Goodbye!")
                break
            elif c == "1":
                s, m = auth.register(
                    input("Name: "),
                    input("Email: "),
                    input("Phone: "),
                    input("Password: "),
                    input("Confirm: ")
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
                        f"\nName: {u.name}\n"
                        f"Email: {u.email}\n"
                        f"Phone: {u.phone}\n"
                        f"Active: {u.is_active}\n"
                        f"Created: {u.created_date}"
                    )
                else:
                    print("Not logged in")
            elif c == "4":
                if auth.current_user:
                    old_password = input("Old Password: ")
                    new_password = input("New Password: ")
                    success, message = auth.current_user.change_password(
                        old_password,
                        new_password
                    )
                    print(message)
                else:
                    print("Not logged in")
            elif c == "5":
                s, m = auth.logout()
                print(m)
            else:
                print("Invalid option. Please choose 0-5.")
        except Exception as e:
            print(f"Something went wrong: {e}")