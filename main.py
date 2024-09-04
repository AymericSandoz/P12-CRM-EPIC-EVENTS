import argparse
from services.auth import login, check_authorization
from services.user_service import create_user
from services.department_service import create_department


def main():
    parser = argparse.ArgumentParser(description="Epic Events CRM CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Commande login : python main.py login luc@example.com securepassword
    login_parser = subparsers.add_parser('login')
    login_parser.add_argument('email', type=str, help='Your email')
    login_parser.add_argument('password', type=str, help='Your password')

    # Commande pour vérifier l'autorisation
    auth_parser = subparsers.add_parser('check')
    auth_parser.add_argument('token', type=str, help='Your JWT token')
    auth_parser.add_argument(
        'permission', type=str, help='The permission to check (create_client, modify_contract, assign_event)')

    # Commande pour créer un utilisateur : python main.py create_user --employee_number 5 --name "John Doe" --email "test@gmail.com" --department_id 6 --password "securepassword" --can_create_clients --can_modify_contracts --can_assign_events
    create_user_parser = subparsers.add_parser('create_user')
    create_user_parser.add_argument(
        '--employee_number', required=True, help='Employee number of the user')
    create_user_parser.add_argument(
        '--name', required=True, help='Name of the user')
    create_user_parser.add_argument(
        '--email', required=True, help='Email of the user')
    create_user_parser.add_argument(
        '--department_id', type=int, required=True, help='Department ID of the user')
    create_user_parser.add_argument(
        '--password', required=True, help='Password for the user')
    create_user_parser.add_argument(
        '--can_create_clients', action='store_true', help='Permission to create clients')
    create_user_parser.add_argument(
        '--can_modify_contracts', action='store_true', help='Permission to modify contracts')
    create_user_parser.add_argument(
        '--can_assign_events', action='store_true', help='Permission to assign events')

    # Commande pour créer un département : python main.py create_department --name "commercial"
    create_department_parser = subparsers.add_parser('create_department')
    create_department_parser.add_argument(
        '--name', required=True, help='Name of the department')

    args = parser.parse_args()

# exemple de commande : python main.py login luc@example.com securepassword
    if args.command == 'login':
        try:
            login(args.email, args.password)
        except Exception as e:  # Remplacez Exception par une exception spécifique si possible
            print(f"Invalid credentials: {e}")
    elif args.command == 'check':
        if check_authorization(args.token, args.permission):
            print("Action authorized.")
        else:
            print("Action not authorized.")

# exemple de commande : python main.py create_user --employee_number 2 --name "Luc  LA" --email "luc@example.com" --department_id 7 --password "securepassword" --can_create_clients --can_modify_contracts --can_assign_events
    elif args.command == 'create_user':
        user_id, user_name = create_user(
            employee_number=args.employee_number,
            name=args.name,
            email=args.email,
            department_id=args.department_id,
            password=args.password,
            can_create_clients=args.can_create_clients,
            can_modify_contracts=args.can_modify_contracts,
            can_assign_events=args.can_assign_events
        )
        print(f"User {user_name} created successfully with ID {user_id}")

    # Commande pour créer un département : python main.py create_department --name "commercial"
    elif args.command == 'create_department':
        department_id, department_name = create_department(args.name)
        print(f"Department {department_name} created successfully with ID {
              department_id}")


if __name__ == "__main__":
    main()
