# python create_user.py --employee_number 12345 --name "John Doe" --email "johndoe@example.com" --department_id 1 --password "securepassword" --can_create_clients --can_modify_contracts --can_assign_events
import argparse
from services.user_service import User_Service


def main():
    parser = argparse.ArgumentParser(
        description="Create a new user in the database.")
    parser.add_argument("--employee_number", required=True,
                        help="Employee number of the user")
    parser.add_argument("--name", required=True, help="Name of the user")
    parser.add_argument("--email", required=True, help="Email of the user")
    parser.add_argument("--department_id", type=int,
                        required=True, help="Department ID of the user")
    parser.add_argument("--password", required=True,
                        help="Password for the user")
    parser.add_argument("--can_create_clients",
                        action="store_true", help="Permission to create clients")
    parser.add_argument("--can_modify_contracts",
                        action="store_true", help="Permission to modify contracts")
    parser.add_argument("--can_assign_events",
                        action="store_true", help="Permission to assign events")

    args = parser.parse_args()

    new_user = User_Service.create(
        employee_number=args.employee_number,
        name=args.name,
        email=args.email,
        department_id=args.department_id,
        password=args.password,
        can_create_clients=args.can_create_clients,
        can_modify_contracts=args.can_modify_contracts,
        can_assign_events=args.can_assign_events
    )

    print(f"User {new_user.name} created successfully with ID {new_user.id}")


if __name__ == "__main__":
    main()
