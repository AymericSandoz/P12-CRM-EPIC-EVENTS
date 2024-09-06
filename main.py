import argparse
from services.auth import login, check_authorization
# from services.user_service import create_user, get_users, get_user
# from services.department_service import create_department, get_departments, get_department
# from services.event_service import get_events, get_event
# from services.client_service import get_clients, get_client
# from services.contract_service import get_contracts, get_contract

from services.user_service import User_Services
from services.department_service import Department_services
from services.event_service import Event_services
from services.client_service import Client_services
from services.contract_service import Contract_services


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

    # Commande pour obtenir tous les utilisateurs
    get_users_parser = subparsers.add_parser('get_users')

    # Commande pour obtenir un utilisateur par ID : python main.py get_user --user_id 1
    get_user_parser = subparsers.add_parser('get_user')
    get_user_parser.add_argument(
        '--user_id', type=int, required=True, help='ID of the user')

    # Commande pour obtenir tous les départements
    get_departments_parser = subparsers.add_parser('get_departments')

    # Commande pour obtenir un département par ID : python main.py get_department --department_id 1
    get_department_parser = subparsers.add_parser('get_department')
    get_department_parser.add_argument(
        '--department_id', type=int, required=True, help='ID of the department')

    # Commande pour obtenir tous les événements
    get_events_parser = subparsers.add_parser('get_events')

    # Commande pour obtenir un événement par ID : python main.py get_event --event_id 1
    get_event_parser = subparsers.add_parser('get_event')
    get_event_parser.add_argument(
        '--event_id', type=int, required=True, help='ID of the event')

    # Commande pour obtenir tous les clients
    get_clients_parser = subparsers.add_parser('get_clients')

    # Commande pour obtenir un client par ID : python main.py get_client --client_id 1
    get_client_parser = subparsers.add_parser('get_client')
    get_client_parser.add_argument(
        '--client_id', type=int, required=True, help='ID of the client')

    # Commande pour obtenir tous les contrats
    get_contracts_parser = subparsers.add_parser('get_contracts')

    # Commande pour obtenir un contrat par ID : python main.py get_contract --contract_id 1
    get_contract_parser = subparsers.add_parser('get_contract')
    get_contract_parser.add_argument(
        '--contract_id', type=int, required=True, help='ID of the contract')

    args = parser.parse_args()

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
    elif args.command == 'create_user':
        user_id, user_name = User_Services.create(
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
    elif args.command == 'create_department':
        department_id, department_name = Department_services.create(args.name)
        print(f"Department {department_name} created successfully with ID {
              department_id}")
    elif args.command == 'get_users':
        users = User_Services.get_all()
        if not users:
            print("No users found.")
        else:
            print(f"There are {len(users)} users")
            for user in users:
                print(f"User ID: {user.id}, Name: {
                      user.name}, Email: {user.email}")
    elif args.command == 'get_user':
        user = User_Services.get(args.user_id)
        if not user:
            print("User not found.")
        else:
            print(f"User ID: {user.id}, Name: {
                  user.name}, Email: {user.email}")
    elif args.command == 'get_departments':
        departments = Department_services.get_all()
        if not departments:
            print("No departments found.")
        else:
            print(f"There are {len(departments)} departments")
            for department in departments:
                print(f"Department ID: {
                      department.id}, Name: {department.name}")
    elif args.command == 'get_department':
        department = Department_services.get()(args.department_id)
        if not department:
            print("Department not found.")
        else:
            print(f"Department ID: {department.id}, Name: {department.name}")
    elif args.command == 'get_events':
        events = Event_services.get_all()
        if not events:
            print("No events found.")
        else:
            print(f"There are {len(events)} events")
            for event in events:
                print(f"Event ID: {event.id}, Name: {event.event_name}")
    elif args.command == 'get_event':
        event = Event_services.get(args.event_id)
        if not event:
            print("Event not found.")
        else:
            print(f"Event ID: {event.id}, Name: {event.event_name}")
    elif args.command == 'get_clients':
        clients = Client_services.get_all()
        if not clients:
            print("No clients found.")
        else:
            print(f"There are {len(clients)} clients")
            for client in clients:
                print(f"Client ID: {client.id}, Name: {client.client_name}")
    elif args.command == 'get_client':
        client = Client_services.get(args.client_id)
        if not client:
            print("Client not found.")
        else:
            print(f"Client ID: {client.id}, Name: {client.client_name}")
    elif args.command == 'get_contracts':
        contracts = Contract_services.get_all()
        if not contracts:
            print("No contracts found.")
        else:
            print(f"There are {len(contracts)} contracts")
            for contract in contracts:
                print(f"Contract ID: {contract.id}, Name: {
                      contract.contract_name}")
    elif args.command == 'get_contract':
        contract = Contract_services.get(args.contract_id)
        if not contract:
            print("Contract not found.")
        else:
            print(f"Contract ID: {contract.id}, Name: {
                  contract.contract_name}")


if __name__ == "__main__":
    main()
