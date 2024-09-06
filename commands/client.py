from services.client_service import Client_services


def add_client_commands(subparsers):
    get_client_parser = subparsers.add_parser('get_client')
    get_client_parser.add_argument(
        '--client_id', type=int, required=True, help='ID of the client')


# create
    create_client_parser = subparsers.add_parser('create_client')
    create_client_parser.add_argument(
        '--full_name', required=True, help='Name of the client')
    create_client_parser.add_argument(
        '--email', required=True, help='Email of the client')
    create_client_parser.add_argument(
        '--phone', required=True, help='Phone number of the client')
    create_client_parser.add_argument(
        '--company_name', required=True, help='Company name of the client')
    create_client_parser.add_argument(
        '--last_contact_date', help='Last contact date of the client')
    create_client_parser.add_argument(
        '--contact_person', required=True, help='Contact person of the client')


def handle_client_commands(args):
    if args.command == 'get_clients':
        clients = Client_services.get_all()
        if not clients:
            print("No clients found.")
        else:
            print(f"There are {len(clients)} clients")
            for client in clients:
                print(f"Client ID: {client.id}, Name: {
                      client.name}, Email: {client.email}")
    elif args.command == 'get_client':
        client = Client_services.get(args.client_id)
        if not client:
            print("Client not found.")
        else:
            print(f"Client ID: {client.id}, Name: {
                  client.name}, Email: {client.email}")

    elif args.command == 'create_client':
        client_id, client_name = Client_services.create(
            name=args.name, email=args.email)
        print(f"Client {client_name} created successfully with ID {client_id}")
