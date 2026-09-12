from modules.auth import Auth
from modules.integration import Integration
from modules.supervisor_dashboard import SupervisorDashboard
from modules.chp_visit import CHPVisit

if __name__ == "__main__":
    print(" BOMAHEALTH")
    print(" Community Health Management System")
    print("Welcome to BomaHealth!")
    print("Please register or login to continue.")
    auth = Auth()
    integration = Integration()
    dashboard = SupervisorDashboard(integration)
    while True:
        print("\n1. Register")
        print("2. Login")
        print("0. Exit")
        choice = input("> ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            success, message = auth.register(
                input("Name: "),
                input("Email: "),
                input("Phone: "),
                input("Password: "),
                input("Confirm: ")
            )
            print(message)
        elif choice == "2":
            success, message = auth.login(
                input("Email: "),
                input("Password: ")
            )
            print(message)
            if success:
                while auth.current_user:
                    print("\n--- Supervisor Menu ---")
                    print("1. Profile")
                    print("2. Change Password")
                    print("3. Add CHP Visit")
                    print("4. View Visits")
                    print("5. View Referrals")
                    print("6. Update Referral")
                    print("7. Logout")
                    option = input("> ").strip()
                    if option == "1":
                        user = auth.current_user
                        print(f"\nName: {user.name}")
                        print(f"Email: {user.email}")
                        print(f"Phone: {user.phone}")
                        print(f"Active: {user.is_active}")
                        print(f"Created: {user.created_date}")
                    elif option == "2":
                        old = input("Old Password: ")
                        new = input("New Password: ")
                        success, message = user.change_password(
                            old, new
                        )
                        print(message)
                    elif option == "3":
                        visit = CHPVisit(
                            input("Visit ID: "),
                            input("CHP ID: "),
                            notes=input("Notes: ")
                        )
                        success, message = integration.sync_visits([visit])
                        print(message)
                    elif option == "4":
                        dashboard.show_visits()
                    elif option == "5":
                        dashboard.show_referrals()
                    elif option == "6":
                        visit_id = input("Visit ID: ")
                        status = input(
                            "Status: "
                        )
                        dashboard.update_referral(
                            visit_id, status
                        )
                    elif option == "7":
                        success, message = auth.logout()
                        print(message)
                    else:
                        print("Invalid option.")
        else:
            print("Invalid option.")